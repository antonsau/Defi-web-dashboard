from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Protocol
from django.db.models import Q
from operator import or_

import pygsheets
import datetime
from functools import reduce

from ..CONFIG import SPREADSHEET_URL, SHEET_NAME, GROUPS, FILTER_TYPES


class ProtocolList(ListView):
    model = Protocol
    context_object_name = 'protocols'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        search_input = self.request.GET.get('search-area')
        if search_input:
            context['protocols'] = context['protocols'].filter(protocol_name__icontains=search_input)
        context['search_input'] = search_input

        # View active protocols by default
        filter_type = self.request.GET.get('status') or 'active'
        if filter_type:
            for group in GROUPS:
                filter_values = FILTER_TYPES.get(filter_type)
                # Ifs are required here, because we need to filter different fields depending on the group
                if group == 'protocols_nodes':
                    context[group] = context['protocols'].filter(reduce(
                        or_, [Q(nodes_st__icontains=f) for f in filter_values]))
                if group == 'protocols_testing':
                    context[group] = context['protocols'].filter(reduce(
                        or_, [Q(testing_st__icontains=f) for f in filter_values]))
                if group == 'protocols_mainnet':
                    context[group] = context['protocols'].filter(reduce(
                        or_, [Q(mainnet_st__icontains=f) for f in filter_values]))

        return context


class ProtocolDetail(DetailView):
    model = Protocol
    context_object_name = 'protocol'
    template_name = 'protocols/protocol.html'


def refresh_protocol_list(request):
    """Deletes all objects in the current model and pull data from the Google Sheet"""

    def convert_date(string_date, input_format, target_format):
        if string_date:
            d = datetime.datetime.strptime(string_date, input_format)
            return d.strftime(target_format)
        return string_date

    def convert_status(string_status):
        if "актив" in str.lower(string_status):
            return True
        return False

    # update data in model (clean and upload)
    Protocol.objects.all().delete()

    client = pygsheets.authorize(service_account_file='service_account.json')
    sheet = client.open_by_url(SPREADSHEET_URL).worksheet('title', SHEET_NAME)
    protocols_data = sheet.get_all_values(include_tailing_empty_rows=False)

    Protocol.objects.bulk_create([Protocol(**{
        'protocol_name': r[0],
        'start_date': convert_date(r[1], '%d/%m/%Y', '%Y-%m-%d'),
        'active_status': convert_status(r[2]),
        'tasks_done': r[3],
        'tasks_pending': r[4],
        'nodes_st': r[5],
        'testing_st': r[6],
        'mainnet_st': r[7],
        # 'transactions_st': r[8],
        # 'performer_1': r[9],
        # 'performer_2': r[10],
        'last_comment': r[11],
    }) for r in protocols_data[1:78]])

    return redirect('protocols')

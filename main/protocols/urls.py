from django.urls import path
from .views import ProtocolList, ProtocolDetail, refresh_protocol_list


urlpatterns = [
    path('protocols', ProtocolList.as_view(), name='protocols'),
    path('protocols/<int:pk>', ProtocolDetail.as_view(), name='protocol'),
    path('refresh', refresh_protocol_list, name='refresh'),
]

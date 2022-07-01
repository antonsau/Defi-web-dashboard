from django.db import models


# Create your models here.
class Protocol(models.Model):
    protocol_name = models.CharField(max_length=100, unique=True)
    start_date = models.CharField(blank=True, max_length=50)
    active_status = models.BooleanField(blank=True)
    tasks_done = models.TextField(blank=True)
    tasks_pending = models.TextField(blank=True)
    nodes_st = models.CharField(blank=True, max_length=100)
    testing_st = models.CharField(blank=True, max_length=100)
    mainnet_st = models.CharField(blank=True, max_length=100)
    transactions_st = models.CharField(blank=True, max_length=100)
    performer_1 = models.CharField(blank=True, max_length=50)
    performer_2 = models.CharField(blank=True, max_length=50)
    last_comment = models.TextField(blank=True)

    def __str__(self):
        return self.protocol_name


class Comment(models.Model):
    protocol_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    comment_text = models.TextField(blank=True, max_length=500)

    def ___str__(self):
        return self.comment_text

from django.db import models
from django.utils import timezone


class Traffic(models.Model):

    date = models.DateField(help_text='date that the traffic object pertains to')
    control_point = models.CharField(max_length=30, help_text='point of entry/exit')
    traffic_id = models.CharField(primary_key=True, unique=True, max_length=41, help_text='primary key, format is {control_point}_{date}')
    weekday = models.CharField(null=True, max_length=9, help_text='day of the week')


class Record(models.Model):

    residents = models.IntegerField(help_text='number of HK residents arriving/departing for the day at this control_point')
    chinavisitors = models.IntegerField(help_text='number of mainland visitors arriving/departing for the day at this control_point')
    othervisitors = models.IntegerField(help_text='number of visitors arriving/departing for the day at this control_point. Does not include residents or visitors from China')
    total = models.IntegerField(help_text='total number of arrivals/departures for the day at this control point. eg: Arrival.total = Arrival.residents + Arrival.mainland_visitors + Arrival.other_visitors')

    class Meta:

        abstract=True


class Arrival(Record):

    traffic = models.OneToOneField(Traffic, related_name='arrivals', on_delete=models.CASCADE, help_text='Traffic model that this Arrival corresponds to. Intended for access through Traffic.arrivals')


class Departure(Record):

    traffic = models.OneToOneField(Traffic, related_name='departures', on_delete=models.CASCADE, help_text='Traffic model that this Departure corresponds to. Intended for access through Traffic.departures')

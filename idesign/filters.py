import django_filters
from .models import Web
from django.contrib.auth.models import User
from django.db import models

from django import forms


class ProductFilter(django_filters.FilterSet):
    area = django_filters.AllValuesFilter()

    # needle = django_filters.AllValuesFilter()
    # stitch = django_filters.AllValuesFilter()

    class Meta:

        model = Web
        fields = ['area']

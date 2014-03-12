from tastypie.resources import ModelResource
from tastypie_optimizers.fields import ToOneFieldNoQuery
from tastypie_optimizers.paginator import RunningCountPaginator

from tastypie_optimizers.models import USState, StarRating, Hotel

import logging

class USStateResource(ModelResource):
    class Meta:
        queryset = USState.objects.all()
        resource_name = 'state'
        allowed_methods = ['get']

class StarRatingResource(ModelResource):
    class Meta:
        queryset = StarRating.objects.all()
        resource_name = 'star_rating'
        allowed_methods = ['get']

class HotelRawResource(ModelResource):
    state = ToOneFieldNoQuery(USStateResource, 'state', full=False, raw_key=True)
    rating = ToOneFieldNoQuery(StarRatingResource, 'rating', full=False, raw_key=True)

    class Meta:
        queryset = Hotel.objects.all()
        resource_name = 'hotel_raw'
        allowed_methods = ['get']
        paginator_class = RunningCountPaginator

class HotelURIResource(ModelResource):
    state = ToOneFieldNoQuery(USStateResource, 'state', full=False, raw_key=False)
    rating = ToOneFieldNoQuery(StarRatingResource, 'rating', full=False, raw_key=False)

    class Meta:
        queryset = Hotel.objects.all()
        resource_name = 'hotel_uri'
        allowed_methods = ['get']
        paginator_class = RunningCountPaginator

class HotelFullResource(ModelResource):
    state = ToOneFieldNoQuery(USStateResource, 'state', full=True)
    rating = ToOneFieldNoQuery(StarRatingResource, 'rating', full=True)

    class Meta:
        queryset = Hotel.objects.select_related('state', 'rating').all()
        resource_name = 'hotel_full'
        allowed_methods = ['get']
        paginator_class = RunningCountPaginator


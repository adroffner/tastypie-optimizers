""" Sample ModelResources demonstrate the optimized resource queries.
"""
from tastypie.resources import ModelResource
from tastypie_optimizers.fields import ToOneFieldNoQuery
from tastypie_optimizers.paginator import RunningCountPaginator

from tastypie_optimizers.models import USState, StarRating, Hotel

import logging

class USStateResource(ModelResource):
    """ US State Codes list, e.g. 'AK' Alaska """
    class Meta:
        queryset = USState.objects.all()
        resource_name = 'state'
        allowed_methods = ['get']

class StarRatingResource(ModelResource):
    """ Hotel Star Rating list, e.g. 5 stars """
    class Meta:
        queryset = StarRating.objects.all()
        resource_name = 'star_rating'
        allowed_methods = ['get']

class HotelRawResource(ModelResource):
    """ A `raw` hotel resource shows the related field's PK only.
    Set: full=False, raw_key=True

    The related field maintains foreign key constraints at the database-level.
    This REST resource can perform all CRUD methods without any nested data.

    {"id": 1, "name": "Best Western", "rating": 3,
     "resource_uri": "/optimizer/v1/hotel_raw/1/",
     "state": "MS"}
    """
    state = ToOneFieldNoQuery(USStateResource, 'state', full=False, raw_key=True)
    rating = ToOneFieldNoQuery(StarRatingResource, 'rating', full=False, raw_key=True)

    class Meta:
        queryset = Hotel.objects.all()
        resource_name = 'hotel_raw'
        allowed_methods = ['get']
        paginator_class = RunningCountPaginator

class HotelURIResource(ModelResource):
    """ A `URI` hotel resource shows the related field's URI to get its resource later.
    Set: full=False, raw_key=False

    The related field maintains foreign key constraints at the database-level.
    This REST resource can perform all CRUD methods without any nested data.

    {"id": 2, "name": "Best Western",
     "rating": "/optimizer/v1/star_rating/2/",
     "resource_uri": "/optimizer/v1/hotel_uri/2/",
     "state": "/optimizer/v1/state/WA/"}
    """
    state = ToOneFieldNoQuery(USStateResource, 'state', full=False, raw_key=False)
    rating = ToOneFieldNoQuery(StarRatingResource, 'rating', full=False, raw_key=False)

    class Meta:
        queryset = Hotel.objects.all()
        resource_name = 'hotel_uri'
        allowed_methods = ['get']
        paginator_class = RunningCountPaginator

class HotelFullResource(ModelResource):
    """ A `full` hotel resource queries the related field's nested resource data.
    Set: full=False, raw_key=True

    The `full` related field acts the same way as the default tastypie.fields.ToOneField.
    This allows some experiments to set `full` or `raw_key` to plan the REST API.

    There are other `optimizations` in this hotel resource.
    1. Use `select_related` to make one joined query, instead of many. 
        Hotel.objects.select_related('state', 'rating').all()
    2. RunningCountPaginator makes no SELECT COUNT(*)... query.
    """
    state = ToOneFieldNoQuery(USStateResource, 'state', full=True)
    rating = ToOneFieldNoQuery(StarRatingResource, 'rating', full=True)

    class Meta:
        queryset = Hotel.objects.select_related('state', 'rating').all()
        resource_name = 'hotel_full'
        allowed_methods = ['get']
        paginator_class = RunningCountPaginator


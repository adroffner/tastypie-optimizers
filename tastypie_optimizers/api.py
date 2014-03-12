from tastypie.api import Api
from resources import (
    USStateResource,
    StarRatingResource,

    HotelRawResource,
    HotelURIResource,
    HotelFullResource
)

v1_api = Api(api_name='v1')

for res in (
    USStateResource,
    StarRatingResource,
    HotelRawResource,
    HotelURIResource,
    HotelFullResource
    ):
    v1_api.register(res())


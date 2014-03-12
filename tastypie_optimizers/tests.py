from django.test import TestCase
from django.test.client import Client
import json

from tastypie_optimizers.models import (
    USState,
    StarRating,
    Hotel
)

class FieldsTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.ma = USState(code='MA', name='Massachusetts')
        self.ma.save()
        self.nj = USState(code='NJ', name='New Jersey')
        self.nj.save()

        self.stars = []
        self.hotels = []
        for r in range(5):
            self.stars.append(StarRating(rating='%d Stars' % (r+1)))
            self.stars[r].save()
            self.hotels.append(Hotel(name='Hotel #%d' % (r+1),
                rating=self.stars[r],
                state=(self.ma if ((r+1) % 2) else self.nj)
            ))
            self.hotels[r].save()

    def test_states(self):
        self.assertEquals(self.ma.code, 'MA')
        self.assertEquals(self.ma.pk, 'MA')
        self.assertEquals(self.nj.code, 'NJ')
        self.assertEquals(self.nj.pk, 'NJ')

    def test_stars(self):
        for r in range(5):
            self.assertEquals(self.stars[r].id, r+1)

    def rest_field_type_ok(self, json_d, fieldname, type_class):
        """ REST resource must have fieldname related resource
        and it must be type_class data-type.
        """
        if fieldname in json_d:
            return isinstance(json_d[fieldname], type_class)
        else:
            return False

    def test_to_one_full(self):
        resp = self.client.get("/optimizer/v1/hotel_full/1/")
        d = json.loads(resp.content)
        self.assertTrue(self.rest_field_type_ok(d, 'state', dict), 'full state required')
        self.assertTrue(self.rest_field_type_ok(d, 'rating', dict), 'full rating required')
        self.assertEquals(d['state'], {
            u'resource_uri': u'/optimizer/v1/state/MA/',
            u'code': u'MA',
            u'name': u'Massachusetts',
        })
        self.assertEquals(d['rating'], {
            u'resource_uri': u'/optimizer/v1/star_rating/1/',
            u'id': 1,
            u'rating': u'1 Stars',
        })

    def test_to_one_uri(self):
        resp = self.client.get("/optimizer/v1/hotel_uri/2/")
        d = json.loads(resp.content)
        self.assertTrue(self.rest_field_type_ok(d, 'state', basestring), 'URI state required')
        self.assertTrue(self.rest_field_type_ok(d, 'rating', basestring), 'URI rating required')
        self.assertEquals(d['state'], u'/optimizer/v1/state/NJ/')
        self.assertEquals(d['rating'], u'/optimizer/v1/star_rating/2/')

    def test_to_one_raw(self):
        resp = self.client.get("/optimizer/v1/hotel_raw/3/")
        d = json.loads(resp.content)
        self.assertTrue(self.rest_field_type_ok(d, 'state', basestring), 'raw state required')
        self.assertTrue(self.rest_field_type_ok(d, 'rating', int), 'raw rating required')
        self.assertEquals(d['state'], u'MA')
        self.assertEquals(d['rating'], 3)


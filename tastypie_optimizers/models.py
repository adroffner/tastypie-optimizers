""" Sample Models demonstrate the optimized resources.
"""
from django.db import models

class USState(models.Model):
    """ US state codes are the primary key, e.g. 'ME', Maine.
    The PK appears as a human readable code in the foreign key.
    """
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=100)


class StarRating(models.Model):
    """ Star Ratings measure numeric id IN(1, 2, ...), with Django's default PK.
    The PK appears as a human readable number in the foreign key.
    """
    rating = models.CharField(max_length=100)


class Hotel(models.Model):
    """ Hotel has both kinds of FK as related fields.
    Its HotelModelResource avoids needless SQL queries
    for `state` and `rating` REST responses.
    """
    name = models.CharField(max_length=100)
    state = models.ForeignKey(USState)
    rating = models.ForeignKey(StarRating)


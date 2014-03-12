from django.db import models

class USState(models.Model):
    """ US state codes are the primary key, e.g. 'ME', Maine.
    The PK appears as a human readable code in the foreign key.
    """
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=100)


class StarRating(models.Model):
    """ Star Ratings measure numerically, id IN(1, 2, ...)i, with PK.
    The PK appears as a human readable number in the foreign key.
    """
    rating = models.CharField(max_length=100)


class Hotel(models.Model):
    """ Hotel has both kind of FK to relate.
    """
    name = models.CharField(max_length=100)
    state = models.ForeignKey(USState)
    rating = models.ForeignKey(StarRating)


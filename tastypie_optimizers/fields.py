from tastypie.fields import ToOneField, NOT_PROVIDED
from tastypie.bundle import Bundle

import logging

class GhostModel(object):
    def __init__(self, pk):
        self.pk = pk

class ToOneFieldNoQuery(ToOneField):
    """
    Provides access to related data via foreign key.
    When full=False, return the URI without a database query.
    Otherwise, return the nested object from the database.

    When full=False and raw_key=True, display the raw foreign key value.
    This can be set to a human-readable key in the related db.Model.

    class RelatedModel(db.Model):
        # id is a meaningful string.
        id = models.CharField(max_length=5, primary_key=True)
        ...

    This subclass requires Django\'s ORM layer to work properly.
    """
    help_text = 'A single related resource. Set a URI without a db query, or query a set of nested resource data.'

    def __init__(self, to, attribute, related_name=None, default=NOT_PROVIDED,
                 null=False, blank=False, readonly=False, full=False,
                 unique=False, help_text=None, use_in='all', full_list=True, full_detail=True,
                 raw_key=False):
        super(ToOneFieldNoQuery, self).__init__(
            to, attribute, related_name=related_name, default=default,
            null=null, blank=blank, readonly=readonly, full=full,
            unique=unique, help_text=help_text, use_in=use_in,
            full_list=full_list, full_detail=full_detail
        )
        self.raw_key=raw_key

    def dehydrate(self, bundle, for_list=True):
        should_dehydrate_full_resource = self.should_full_dehydrate(bundle, for_list=for_list)

        if not should_dehydrate_full_resource:
            pk = getattr(bundle.obj, "%s_id" % self.attribute, None)
            if self.raw_key:
                return pk
            else:
                b = Bundle(obj=GhostModel(pk))
                return self.to().get_resource_uri(b)

        return super(ToOneFieldNoQuery, self).dehydrate(bundle, for_list=for_list)


class ToOneField(ToOneFieldNoQuery):
    pass


class ForeignKey(ToOneFieldNoQuery):
    pass


class OneToOneField(ToOneFieldNoQuery):
    pass


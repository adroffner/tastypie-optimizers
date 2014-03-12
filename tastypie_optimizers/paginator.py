from tastypie.paginator import Paginator

class RunningCountPaginator(Paginator):
    """ Show a "running count" of the results so far.
    This doesn't require an extra SELECT COUNT(*) FROM ...
    """
    def get_count(self):
        return -1

    def page(self):
        """ Count all the objects on the pages before current one,
        and add the remaining objects to make a running count.

        When pages fall over the end, running_count = -1
        """
        data = super(RunningCountPaginator, self).page()
        try:
            obj_count = len(data[self.collection_name])
            if obj_count:
                obj_count += self.get_offset()
            else:
                obj_count = -1
            data['meta']['running_count'] = obj_count
            del data['meta']['total_count']
        except KeyError:
            pass
        return data


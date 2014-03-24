from django.db import models

class TransformQuerySetMixin(object):
    def __init__(self, *args, **kwargs):
        super(TransformQuerySetMixin, self).__init__(*args, **kwargs)
        self._transform_fns = []

    def _clone(self, klass=None, setup=False, **kw):
        c = super(TransformQuerySetMixin, self)._clone(klass, setup, **kw)
        c._transform_fns = self._transform_fns[:]
        return c

    def transform(self, fn):
        c = self._clone()
        c._transform_fns.append(fn)
        return c

    def iterator(self):
        result_iter = super(TransformQuerySetMixin, self).iterator()
        if self._transform_fns:
            results = list(result_iter)
            for fn in self._transform_fns:
                fn(results)
            return iter(results)
        return result_iter


class TransformQuerySet(TransformQuerySetMixin, models.query.QuerySet):
    pass


class TransformManager(models.Manager):
    def get_query_set(self):
        return TransformQuerySet(self.model)

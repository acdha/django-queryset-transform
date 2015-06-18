from django.db import models


class TransformQuerySetMixin(object):
    def __init__(self, *args, **kwargs):
        super(TransformQuerySetMixin, self).__init__(*args, **kwargs)
        self._transform_fns = []

    def _clone(self, klass=None, setup=False, **kwargs):
        c = super(TransformQuerySetMixin, self)._clone(klass, setup, **kwargs)
        c.__dict__.update(kwargs)
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

    def values(self, *fields):
        new_qs = self._clone(klass=TransformValuesQuerySet, setup=True, _fields=fields)
        # We have to clear any existing transforms as they will expect a different result type
        # but want to allow adding new ones:
        del new_qs._transform_fns[:]
        return new_qs

    def values_list(self, *fields, **kwargs):
        flat = kwargs.pop('flat', False)

        if kwargs:
            raise TypeError('Unexpected keyword arguments to values_list: %s' % (list(kwargs),))

        if flat and len(fields) > 1:
            raise TypeError("'flat' is not valid when values_list is called with more than one field.")

        new_qs = self._clone(klass=TransformValuesListQuerySet, setup=True, _fields=fields, flat=flat)
        # We have to clear any existing transforms as they will expect a different result type
        # but want to allow adding new ones:
        del new_qs._transform_fns[:]
        return new_qs


class TransformQuerySet(TransformQuerySetMixin, models.query.QuerySet):
    pass


class TransformValuesQuerySet(TransformQuerySetMixin, models.query.ValuesQuerySet):
    pass


class TransformValuesListQuerySet(TransformQuerySetMixin, models.query.ValuesListQuerySet):
    pass


class TransformManager(models.Manager):
    def get_queryset(self):
        return TransformQuerySet(self.model)

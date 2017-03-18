class BaseAdapter(object):
    def can_use_adapter(self):
        raise NotImplementedError

    def adapt(self, obj, child):
        raise NotImplementedError


class DictAdapter(BaseAdapter):
    def __init__(self, dict_name):
        self._dict_name = dict_name

    def can_use_adapter(self, obj):
        return hasattr(obj, self._dict_name)

    def adapt(self, obj, child):
        return getattr(obj, self._dict_name)[child]


class FnAdapter(BaseAdapter):
    def __init__(self, fn_name):
        self._fn_name = fn_name

    def can_use_adapter(self, obj):
        return hasattr(obj, self._fn_name)

    def adapt(self, obj, child):
        return getattr(obj, self._fn_name)(child)



import attr


@attr.s(slots=True)
class Tuple:

    def __getitem__(self, item_key):
        return attr.astuple(self)[item_key]

    def __iter__(self):
        return iter(attr.astuple(self))

    def evolve(self, **kwargs):
        return attr.evolve(self, **kwargs)

    def transform(self, **kwargs):
        return attr.evolve(
            self,
            {k: f(getattr(self, k))for k, f in kwargs.items()})

    def asdict(self):
        return attr.asdict(self)


# @attr.s(slots=True)
# class CurrPrev(Tuple):
#     curr = attr.ib()
#     prev = attr.ib()


# @attr.s(slots=True)
# class CurrNext(Tuple):
#     curr = attr.ib()
#     next = attr.ib()


# @attr.s(slots=True)
# class ValueIndex(Tuple):
#     value = attr.ib()
#     index = attr.ib()


# @attr.s(slots=True)
# class KeyValues(Tuple):
#     key = attr.ib()
#     values = attr.ib()


class Row(tuple):
    def __new__(self, **kwargs):
        row = tuple.__new__(self, kwargs.values())
        row._dict = kwargs
        row._fields = set(kwargs.keys())

        return row

    def __getattribute__(self, name):
        if name in tuple.__getattribute__(self, '_fields'):
            # Accessing Row fields has higher priority
            # than accessing tuple methods
            return tuple.__getattribute__(self, '_dict')[name]
        else:
            return tuple.__getattribute__(self, name)

    # def __getattr__(self, name):
    #     if name in self._dict:
    #         return self._dict[name]
    #     else:
    #         raise AttributeError(f'{self!r} has no attribute {name!r}')

    def evolve(self, **kwargs):
        d = self._dict.copy()
        d.update(kwargs)
        return Row(**d)

    def transform(self, **kwargs):
        d = self._dict.copy()
        d.update({k: f(getattr(self, k))for k, f in kwargs.items()})
        return Row(**d)

    def asdict(self):
        return self._dict.copy()

    def __repr__(self):
        kwargs_str = ', '.join(f'{k}={v!r}' for k, v in self._dict.items())
        return f'Row({kwargs_str})'


class namedrow:

    def __init__(self, *fields):
        self._fields = fields

    def __call__(self, *args, **kwargs):
        if args and kwargs:
            raise ValueError(
                'Cannot use both args and kwargs to create {type(self)}')

        if args:
            return Row(**{field: value
                          for field, value in zip(self._fields, args)})

        if kwargs:
            return Row(**{field: kwargs[field] for field in self._fields})


CurrPrev = namedrow('curr', 'prev')
CurrNext = namedrow('curr', 'prev')
ValueIndex = namedrow('value', 'index')
KeyValues = namedrow('key', 'values')
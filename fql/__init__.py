from simplejson import dumps

class Field(object):
    def __init__(self, name=None, index=False):
        self.index = index
        self.name = name

    def coerce(self):
        raise NotImplementedError

class String(Field):
    def coerce(self, from_facebook):
        if not isinstance(from_facebook, unicode):
            from_facebook = unicode(from_facebook, 'utf-8')
        return from_facebook

class TableMeta(type):
    def __init__(cls, name, bases, d):
        super(TableMeta, cls).__init__(name, bases, d)
        if bases:
            for field_name, field in d.iteritems():
                if isinstance(field, Field):
                    field.name = field_name

    @property
    def _fields(cls):
        return tuple(
            f for _, f in cls.__dict__.iteritems() if isinstance(f, Field)
        )

    @property
    def _indexes(cls):
        return tuple(i for i in cls._fields if i.index)

    @property
    def _index_keys(cls):
        return tuple(i.name for i in cls._indexes)

    def query(cls, **where):
        print cls._fields, cls._indexes, cls._index_keys
        if not where:
            raise ValueError('%s.query needs index' % cls.__name__)
        for i in where:
            if i in cls._index_keys:
                break
        else:
            raise ValueError('Need at least one parimay index')
        print "SELECT %s FROM %s WHERE % s" % (
            ', '.join(field.name for field in cls._fields),
            cls.__tablename__,
            ', '.join("%s = %s" % (k, dumps(v)) for k, v in where.iteritems())
        )

Table = TableMeta('TableMeta', (), {})

class Page(Table):
    __tablename__ = 'page'
    about = String()
    name = String(index=True)

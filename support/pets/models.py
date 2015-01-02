from google.appengine.ext import ndb


class Pet(ndb.Model):
    """The Pet class provides storage for pets.

    >>> # initialize testbed stubs
    >>> testbed.init_memcache_stub()
    >>> testbed.init_datastore_v3_stub()

    You can create a pet:
    >>> muffy = Pet(name=u'muffy', type=u'dog', breed=u"Shi'Tzu")
    >>> muffy # doctest: +ELLIPSIS
    Pet(name=u'muffy', type=u'dog', breed=u"Shi'Tzu", ...)
    >>> muffy_key = muffy.put()

    Once created, you can load a pet by its key:

    >>> muffy_key.get() # doctest: +ELLIPSIS
    Pet(name=u'muffy', type=u'dog', breed=u"Shi'Tzu", ...)

    Or by a query that selects the pet:

    >>> list(Pet.query(Pet.type == 'dog')) # doctest: +ELLIPSIS
    [Pet(name=u'muffy', ...)]

    To modify a pet, change one of its properties and ``put()`` it again.

    >>> muffy_2 = muffy
    >>> muffy_2.age = 10
    >>> muffy_key_2 = muffy_2.put()

    The pet's key doesn't change when it is updated.

    >>> bool(muffy_key == muffy_key_2)
    True
    """
    name = ndb.StringProperty(required=True)
    type = ndb.StringProperty(required=True, choices=("cat", "dog", "bird", "fish", "monkey"))
    breed = ndb.StringProperty()
    age = ndb.IntegerProperty()
    comments = ndb.TextProperty()
    created = ndb.DateTimeProperty(auto_now_add=True, required=True)

    def __repr__(self):
        return ("Pet(name=%r, type=%r, breed=%r, age=%r, "
                "comments=%r, created=%r)" %
                (self.name, self.type, self.breed, self.age,
                 self.comments, self.created))

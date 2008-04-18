from google.appengine.ext import db

class Pet(db.Model):
    """
    The Pet class provides storage for pets. You can create a pet:

    >>> muffy = Pet(name=u'muffy', type=u'dog', breed=u"Shi'Tzu")
    >>> muffy # doctest: +ELLIPSIS
    Pet(name=u'muffy', type=u'dog', breed=u"Shi'Tzu", ...)
    >>> muffy_key = muffy.put()

    Once created, you can load a pet by its key:

    >>> Pet.get(muffy_key) # doctest: +ELLIPSIS
    Pet(name=u'muffy', type=u'dog', breed=u"Shi'Tzu", ...)

    Or by a query that selects the pet:

    >>> list(Pet.all().filter('type = ', 'dog')) # doctest: +ELLIPSIS
    [Pet(name=u'muffy', ...)]

    To modify a pet, change one of its properties and ``put()`` it again.

    >>> muffy_2 = _[0]
    >>> muffy_2.age = 10
    >>> muffy_key_2 = muffy_2.put()

    The pet's key doesn't change when it is updated.

    >>> bool(muffy_key == muffy_key_2)
    True
    """
    name = db.StringProperty(required=True)
    type = db.StringProperty(required=True,
                             choices=set(["cat", "dog", "bird",
                                          "fish", "monkey"]))
    breed = db.StringProperty()
    age = db.IntegerProperty()
    comments = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True, required=True)

    def __repr__(self):
        return ("Pet(name=%r, type=%r, breed=%r, age=%r, "
                "comments=%r, created=%r)" %
                (self.name, self.type, self.breed, self.age,
                 self.comments, self.created))

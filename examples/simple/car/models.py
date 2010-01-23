## TODO: update for django 1.0+

from django.db import models
from django_history_tables import HistoryModel, HistoryManager, history_save

class Manufacturer(models.Model):
    name = models.CharField(max_length=64, default="VW")
    def __unicode__(self):
        return u"<manufacturer name=%s>" % (self.name)
    
    class Admin: pass

class Color(models.Model):
    name = models.CharField(max_length=64, default="Green")
    def __unicode__(self):
        return u"<color name=%s>" % (self.name)
    
    class Admin:
        pass

class Car(models.Model):
    foo = models.CharField(max_length=64, default="foo")
    bar = models.TextField(default="bar")
    maker = models.ForeignKey(Manufacturer)
    colors = models.ManyToManyField(Color)
    slug = models.SlugField(unique=True)
    desc = models.TextField()

    objects = models.Manager()
    history = HistoryManager()

    def __unicode__(self):
        return u"<car foo=%s bar=%s maker=%s colors=%s slug=%s>" % (self.foo, self.bar, self.maker, self.colors, self.slug)

    class Admin:
        pass

class CarHistory(HistoryModel):
    class History:
        model = Car

    def __unicode__(self):
        return u"<carhistory revision=%s>" % self.history_revision

    class Admin:
        pass

def carhistory_save(sender, instance, signal, *args, **kwargs):
    history_model = CarHistory
    history_save(sender, instance, signal, history_model, *args, **kwargs)

from django.db.models.signals import pre_delete, pre_save
pre_save.connect(carhistory_save, sender=Car)
pre_delete.connect(carhistory_save, sender=Car)



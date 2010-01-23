#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.base import ModelBase
from django.utils.translation import ugettext_lazy as _
#from django.contrib.auth.models import User
from django_history_tables.managers import HistoryModelManager

import copy
import datetime

class HistoryModelBase(ModelBase):
    def __new__(cls, name, bases, dct):
        new_class = ModelBase.__new__(cls, name, bases, dct)
        if 'History' in dct:
            history_model = dct['History'].model
            for field in history_model._meta.fields:
                if field.__class__.__name__ == 'AutoField':
                    continue
                #if getattr(field, 'related_name', None):
                #    #print field.related_name
                #    pass
                _field = copy.deepcopy(field)
                if getattr(_field, 'unique', False):
                    try:
                        _field.unique = False
                    except AttributeError:
                        # newer Django defines unique as a property
                        # that uses _unique to store data.  We're
                        # jumping over the fence by setting _unique,
                        # so this sucks, but this happens early enough
                        # to be safe.
                        _field._unique = False
                rel = getattr(_field, 'rel', None)
                if rel and rel.related_name:
                    rel.related_name = rel.related_name + "history"
                new_class.add_to_class(_field.name, _field)
            for mm in history_model._meta.many_to_many:
                _mm = copy.deepcopy(mm)
                if getattr(_mm, 'unique', False):
                    try:
                        _mm.unique = False
                    except AttributeError:
                        # newer Django defines unique as a property
                        # that uses _unique to store data.  We're
                        # jumping over the fence by setting _unique,
                        # so this sucks, but this happens early enough
                        # to be safe.
                        _mm._unique = False
                rel= getattr(_mm, 'rel', None)
                if rel and rel.related_name:
                    rel.related_name = rel.related_name + "history"
                if rel and rel.through:
                    # Will not remain in history table, other wise will report error
                    rel.through = rel.through + "History"
                else:
                    new_class.add_to_class(_mm.name, _mm)
            # insert new class into original object for backreference
            history_model.add_to_class("history_model", new_class)
        return new_class
    
class HistoryModel(models.Model):
    __metaclass__ = HistoryModelBase

    history_datetime = models.DateTimeField(default=datetime.datetime.now)
    history_objectid = models.PositiveIntegerField() # these two are
    history_revision = models.PositiveIntegerField() # unique_together ?
    history_comment = models.CharField(max_length=1024, default="")
#    history_operatedby =   models.ForeignKey(User)
#    
#    def pre_save(self, request):
#        if not self.id:
#            self.history_operatedby = request.user

    def __unicode__(self):
        return u"<history revision=%s>" % self.history_revision

    objects = HistoryModelManager()
    
    class Meta:
        abstract = True

def history_save(sender, instance, signal, history_model, *args, **kwargs):
    if not instance.id:
        # initial save, don't have to do anything :)
        return
    # lookup orginal unchanged object
    orginal = sender.objects.get(pk=instance.id)

    # copy orginal object into history
    history_obj = history_model()
    history_obj.history_objectid = orginal.id
    history_obj.history_revision = history_model.objects.filter(history_objectid=orginal.id).count()+1
    history_obj.history_comment = "pre_save history item <%s>" % (repr(orginal))
    
    for field in orginal._meta.fields:
        if field.__class__.__name__ == 'AutoField':
            continue
        setattr(history_obj, field.name, getattr(orginal, field.name))
    history_obj.save()
    for mm in orginal._meta.many_to_many:
        setattr(history_obj, mm.name, getattr(orginal, mm.name).all())
    history_obj.save()


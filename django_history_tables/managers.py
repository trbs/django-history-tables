from django.db.models.query import QuerySet, EmptyQuerySet
from django.db.models import Manager

class HistoryModelManager(Manager):
    def get_last(self):
        return self.get_query_set().order_by('-history_revision')[0]
    
    def get_first(self):
        return self.get_query_set().order_by('history_revision')[0]
    
    def get_revision(self, revision):
        return self.get_query_set().get(history_revision=revision)

class HistoryManager(HistoryModelManager):
    def get_empty_query_set(self):
        return EmptyQuerySet(self.model.history_model)
    
    def get_query_set(self):
        return QuerySet(self.model.history_model)
    
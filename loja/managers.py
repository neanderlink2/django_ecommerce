from django.db import models
from loja.querysets import ProdutoQuerySet

class ProdutoManager(models.Manager):
    def get_queryset(self):
        return ProdutoQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()

    def search(self, search):
        return self.get_queryset().active().search(search)
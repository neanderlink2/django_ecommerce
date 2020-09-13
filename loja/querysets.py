from django.db import models
from django.db.models import Q

class ProdutoQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self, search):
        lookups = Q(title__contains=search) | Q(description__contains=search)
        return self.filter(lookups).distinct()
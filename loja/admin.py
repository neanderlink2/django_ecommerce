from django.contrib import admin
from loja.models import Produto, Tag, Categoria

# Register your models here.
class Produtos(admin.ModelAdmin):
    list_display = ('id', 'slug', 'title', 'price', 'description',)
    list_display_links = ('id','title',)
    search_fields = ('title',)

class Tags(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('title',)
    search_fields = ('title','slug',)

class Categorias(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('title',)
    search_fields = ('title','slug',)


admin.site.register(Produto, Produtos)
admin.site.register(Tag, Tags)
admin.site.register(Categoria, Categorias)
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser


from loja.models import Produto, Tag, PedidoCliente, Categoria
from loja.serializers import ProdutoSerializer, TagSerializer, PedidoClienteSerializer, CategoriaSerializer
from loja.permissions import CreanteAndReadOnly, IsAdminOrReadOnly

class ProdutosViewSet(viewsets.ModelViewSet):
   queryset = Produto.objects.all()
   serializer_class = ProdutoSerializer
   lookup_field = 'slug'
   filter_backends = (filters.SearchFilter,)
   search_fields = ['title', 'description']
   permission_classes = [IsAdminOrReadOnly]

   @action(detail=False)
   def featured(self, request):
      produtos = Produto.objects.featured()
      serializer = self.get_serializer(produtos, many=True)
      return Response(serializer.data)

   @action(detail=False)
   def active(self, request):
      produtos = Produto.objects.active()
      serializer = self.get_serializer(produtos, many=True)
      return Response(serializer.data)

   @action(detail=False)
   def search(self, request):
      search = request.GET.get('q', None)
      produtos = []
      if search is not None:
         produtos = Produto.objects.search(search)
      produtos = produtos if produtos else Produto.objects.featured()
      serializer = self.get_serializer(produtos, many=True)
      return Response(serializer.data)

class TagViewSet(viewsets.ModelViewSet):
   queryset = Tag.objects.all()
   serializer_class = TagSerializer
   permission_classes = [IsAdminUser, IsAuthenticated]


class PedidosViewSet(viewsets.ModelViewSet):
   serializer_class = PedidoClienteSerializer
   permission_classes = [IsAuthenticated, CreanteAndReadOnly]

   def get_queryset(self):
      if not self.request.user.is_superuser:
         return PedidoCliente.objects.all().filter(user=self.request.user)
      return PedidoCliente.objects.all()


class CategoriasViewSet(viewsets.ModelViewSet):
   queryset = Categoria.objects.all()
   serializer_class = CategoriaSerializer
   permission_classes = [IsAdminUser, IsAuthenticated]

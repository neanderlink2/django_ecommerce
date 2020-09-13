from rest_framework import serializers
from loja.models import Produto, Tag, PedidoCliente, Categoria, PedidoProduto


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id','title','slug']

class ProdutoSerializer(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField(source='categoria', read_only=True)
    class Meta: 
        model = Produto
        fields = ['id', 'title', 'description', 'price', 'image', 'active', 'categoria', 'category_name','featured', 'slug']
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field':'slug'}}

class TagSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Tag
        fields = ['id', 'title', 'slug', 'active']

class CarrinhoSerializer(serializers.Serializer):
    quantidade = serializers.IntegerField(default=1)
    produto_id = serializers.IntegerField(required=False)


class PedidoClienteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    produtos = ProdutoSerializer(many=True, read_only=True)
    carrinho = serializers.ListField(child=CarrinhoSerializer(), write_only=True, required=False, default=[])

    class Meta:
        model = PedidoCliente
        fields = ['id', 'total', 'numero_confimacao', 'user', 'produtos', 'carrinho']

    def __add_produdtos(self, produtos, pedido_id):
        for produto in produtos:
            if "quantidade" not in produto and "produto_id" not in produto:
                continue
            PedidoProduto.objects.create(
                pedido_cliente_id=pedido_id,
                produto_id=produto["produto_id"],
                quantidade=produto["quantidade"]
            )

    def create(self, validated_data):
        produtos = validated_data.pop('carrinho',[])
        pedido = PedidoCliente.objects.create(**validated_data)
        self.__add_produdtos(produtos, pedido.id)
        return pedido


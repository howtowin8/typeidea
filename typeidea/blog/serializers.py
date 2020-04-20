from rest_framework import serializers

from .models import Post,Category,Tag

from rest_framework import pagination

class PostSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field ='name'
    )

    tag = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
    )

    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',

    )
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Post
        fields=('id','title','category','tag','owner','created_time')


class PostDetailSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ['url','id','title','category','tag','owner','content_html','created_time']
        extra_kwargs ={
            'url':{'view_name':'api-post-detail'}
        }


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id','name','created_time',
        )

class CategoryDetailSerializer(CategorySerializer):
    posts = serializers.SerializerMethodField('paginated_posts')

    def paginated_posts(self,obj):
        posts = obj.post_set.filter(status= Post.STATUS_NORMAL)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(posts,self.context['request'])
        serializers = PostSerializer(page,many=True,context={
            'request':self.context['request']
        })
        return {
            'count':posts.count(),
            'results':serializers.data,
            'previous':paginator.get_previous_link(),
            'next':paginator.get_next_link(),
        }

    class Meta:
        model = Category
        fields = (
            'url','id','name','created_time','posts'
        )
        extra_kwargs={
            'url':{'view_name':'api-category-detail'}
        }


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('id','name','created_time')

class TagDetailSerializer(TagSerializer):
    posts = serializers.SerializerMethodField('paginated_posts')

    def paginated_posts(self, obj):
        posts = obj.post_set.filter(status=Post.STATUS_NORMAL)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(posts, self.context['request'])
        serializers = PostSerializer(page, many=True, context={
            'request': self.context['request']
        })
        return {
            'count': posts.count(),
            'results': serializers.data,
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link(),
        }

    class Meta:
        model = Category
        fields = (
            'url', 'id', 'name', 'created_time', 'posts'
        )
        extra_kwargs = {
            'url': {'view_name': 'api-tag-detail'}
        }

import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User

from posts.models import Category, Topic, Post

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "description")


class TopicType(DjangoObjectType):
    class Meta:
        model = Topic
        fields = ("id", "name", "category", "created")

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username")

class PostType(DjangoObjectType):
    createdBy = graphene.Field(UserType)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "text",
            "slug",
            "topic",
            "created_at",
            "updated_at",
            "created_by",
        )

    def resolve_createdBy(root, info):
        return root.created_by



class Query(graphene.ObjectType):
    all_categories = graphene.List(CategoryType)
    all_topics = graphene.List(TopicType)
    all_posts = graphene.List(PostType)

    category_by_id = graphene.Field(CategoryType, id=graphene.Int(required=True))
    topic_by_id = graphene.Field(TopicType, id=graphene.Int(required=True))
    post_by_id = graphene.Field(PostType, id=graphene.Int(required=True))

    posts_by_title_contains = graphene.List(PostType, substr=graphene.String(required=True))

    posts_by_username = graphene.List(PostType, username=graphene.String(required=True))

    posts_count_by_user_id = graphene.Int(user_id=graphene.Int(required=True))

    def resolve_all_categories(root, info):
        return Category.objects.all()

    def resolve_all_topics(root, info):
        return Topic.objects.select_related("category").all()

    def resolve_all_posts(root, info):
        return Post.objects.select_related("topic", "created_by").all()

    def resolve_category_by_id(root, info, id):
        return Category.objects.get(pk=id)

    def resolve_topic_by_id(root, info, id):
        return Topic.objects.get(pk=id)

    def resolve_post_by_id(root, info, id):
        return Post.objects.get(pk=id)

    def resolve_posts_by_title_contains(root, info, substr):
        return Post.objects.filter(title__icontains=substr)

    def resolve_posts_by_username(root, info, username):
        return Post.objects.filter(created_by__username=username)

    def resolve_posts_count_by_user_id(root, info, user_id):
        return Post.objects.filter(created_by_id=user_id).count()


class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        text = graphene.String(required=True)
        slug = graphene.String(required=True)
        topic_id = graphene.Int(required=True)
        created_by_id = graphene.Int(required=False)

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, title, text, slug, topic_id, created_by_id=None):
        topic = Topic.objects.get(pk=topic_id)

        user = None
        if created_by_id is not None:
            user = User.objects.get(pk=created_by_id)
        elif info.context.user.is_authenticated:
            user = info.context.user

        post = Post.objects.create(
            title=title,
            text=text,
            slug=slug,
            topic=topic,
            created_by=user
        )
        return CreatePost(post=post)

class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String(required=False)
        text = graphene.String(required=False)
        slug = graphene.String(required=False)

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, id, title=None, text=None, slug=None):
        post = Post.objects.get(pk=id)

        if title is not None:
            post.title = title
        if text is not None:
            post.text = text
        if slug is not None:
            post.slug = slug

        post.save()
        return UpdatePost(post=post)

class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            post = Post.objects.get(pk=id)
            post.delete()
            return DeletePost(ok=True)
        except Post.DoesNotExist:
            return DeletePost(ok=False)

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)


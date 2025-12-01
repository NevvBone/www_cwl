from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Topic, Post
from django.utils import timezone
import re

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=60)
    description = serializers.CharField(required=False)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        if 'created_at' in validated_data:
            instance.created_at = validated_data['created_at']
        instance.save()
        return instance


class TopicSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    class Meta:
        model = Topic
        fields = ['id', 'name', 'category','category_id', 'created']
        read_only_fields = ['id', 'created']


class PostSerializer(serializers.ModelSerializer):
    topic_id = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(),
        source='topic',
        write_only=True
    )

    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'topic', 'topic_id', 'slug',
                  'created_at', 'updated_at', 'created_by']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']

    def validate_title(self, value):
        if not re.match(r'^[A-Za-z ]+$', value):
            raise serializers.ValidationError("Nazwa może zawierać tylko litery.")
        return value

    def validate_created_at(self, value):
        if value and value > timezone.now():
            raise serializers.ValidationError("Data dodania nie może wybiegać w przyszłość.")
        return value

    def create(self, validated_data):
        # created_by dodajemy w widoku
        return Post.objects.create(**validated_data)

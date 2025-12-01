```python
from posts.models import Category, Topic, Post
from posts.serializers import CategorySerializer, TopicSerializer, PostSerializer
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io

category = Category.objects.create(name="Tech", description="Technology news")

serializer = CategorySerializer(category)
print("Serialized Category:", serializer.data)

json_bytes = JSONRenderer().render(serializer.data)
print("JSON:", json_bytes)
stream = io.BytesIO(json_bytes)
data = JSONParser().parse(stream)

deserializer = CategorySerializer(data=data)
print("is_valid():", deserializer.is_valid())
print("validated_data:", deserializer.validated_data)

topic = Topic.objects.create(name="Mechanisms", category=category)
topic_serializer = TopicSerializer(topic)
print("Serialized Topic:", topic_serializer.data)

user = User.objects.first()

post_data = {
    "title": "Mechanics of AI",
    "text": "This post explains mechanisms...",
    "slug": "mechanics-of-ai",
    "topic_id": topic.id,
    "created_by_id": user.id,
}

post_serializer = PostSerializer(data=post_data)

print("Post valid?:", post_serializer.is_valid())
print("Post errors:", post_serializer.errors)

if post_serializer.is_valid():
    new_post = post_serializer.save()
    print("Saved Post:", PostSerializer(new_post).data)
```


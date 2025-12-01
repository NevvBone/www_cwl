```python
from blog.models import Category, Post, Topic
from blog.serializers import CategorySerializer, PostSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io

category = Category.objects.create(name="Tech", description="Technology news")
topic = Topic.objects.create(name="Mechanism", category=category)

serializer1 = CategorySerializer(cat)
print("CategorySerializer.data:", serializer.data) 

serializer2 = TopicSerializer(topic)
print(serializer2.data)

json_content = JSONRenderer().render(serializer.data)
print("JSON:", json_content)

stream = io.BytesIO(json_content)
data = JSONParser().parse(stream)


deserializer = CategorySerializer(data=data)
print("is_valid():", deserializer.is_valid())
print("validated_data:", deserializer.validated_data)
data['topic_id'] = topic.id  
data['created_by_id'] = user.id

deserializer = PostSerializer(data=data)

if deserializer.is_valid():  
   new_post = deserializer.save()  
   print('Saved without errors')  
   print(PostSerializer(new_post).data)  
else:  
   print('Errors:')  
   print(deserializer.errors)
```


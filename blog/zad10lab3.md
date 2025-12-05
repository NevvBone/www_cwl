- punkt 1  
 `Category.objects.all()\`  
- punkt 2  
 `Category.objects.get(id=3)\`  
- punkt 3  
 `Category.objects.filter(name\_\_startswith='N')\`  
- punkt 4  
 `Topic.objects.values\_list('category\_\_name', flat=True).distinct()\`  
- punkt 5  
 `Post.objects.order\_by('-title').values\_list('title', flat=True)\`  
- punkt 6  
 `Category.objects.create(name='Source')\`  

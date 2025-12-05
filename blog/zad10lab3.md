- punkt 1  
 `Category.objects.all()`  
- punkt 2  
 `Category.objects.get(id=3)`  
- punkt 3  
 `Category.objects.filter(name__startswith='N')`  
- punkt 4  
 `Topic.objects.values_list('category__name', flat=True).distinct()`  
- punkt 5  
 `Post.objects.order_by('-title').values_list('title', flat=True)`  
- punkt 6  
 `Category.objects.create(name='Source')`  

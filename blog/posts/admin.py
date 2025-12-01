from django.contrib import admin
from .models import Category, Topic, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_text', 'topic_category', 'slug', 'created_at', 'updated_at', 'created_by',)
    list_filter = ('topic', 'topic__category', 'created_by',)
    readonly_fields = ('created_at',)
    prepopulated_fields = {'slug': ('title',)}

    def short_text(self, obj):
        words = obj.text.split()
        short_text = ' '.join(words[:5])
        if len(words) > 5:
            short_text += '...'
        return short_text

    short_text.short_description = "Treść skrócona"

    @admin.display(description="Topic (Category)")
    def topic_category(self, obj):
        return f"{obj.topic.name} ({obj.topic.category.name})"
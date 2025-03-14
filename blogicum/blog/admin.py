from django.contrib import admin

from .models import Category, ComentPosts, Location, Post


class CategoryAdmin(admin.ModelAdmin):
    ...


class LocationAdmin(admin.ModelAdmin):
    ...


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'pub_date',
        'is_published',
        'category',
    )


class ComentPostsAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'post',
        'created_at',
        'author',
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(ComentPosts, ComentPostsAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)

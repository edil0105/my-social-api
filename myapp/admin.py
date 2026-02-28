from django.contrib import admin
# models.py ішіндегі класс аттарын дәл жазу керек
from .models import Post, Comment, Like, Follow, Media 

# Әр модельді жеке тіркеу
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'caption', 'created_at') # Бұл кестеде бағандарды әдемі көрсетеді

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'created_at')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post')

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'following')

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'file')

# Егер арнайы User моделің болса, оны да қосу керек
# Бірақ стандартты User болса, ол онсыз да тұр
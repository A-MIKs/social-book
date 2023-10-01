from django.contrib import admin
from .models import FollowUser, LikePost,Profile, Post
# Register your models here.
admin.site.register(LikePost)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(FollowUser)
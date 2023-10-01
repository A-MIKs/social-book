from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import uuid

class FollowUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followings")
    
    def __str__(self):
        return self.user.username
    

class LikePost(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(
        upload_to="profile_images", default="blank-profile-picture.png"
    )
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
    @property
    def followers(self):
        followers =  self.user.followers.all()
        return [follower.follower for follower in followers]
    @property
    def followings(self):
        followings =  self.user.followings.all()
        return [following.user for following in followings]



class Post(models.Model):
    class Meta:
        ordering = ["-created_at"]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="post_images")
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.PositiveBigIntegerField(default=0)

    @property
    def likedUsers(self):
        likes = self.likepost_set.all()
        return [like.user for like in likes]

            
    def __str__(self):
        return self.user.username

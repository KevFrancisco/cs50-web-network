from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm
from django import forms

from cloudinary.models import CloudinaryField


class User(AbstractUser):
    pass


class Post(models.Model):
    owner = models.ForeignKey(
        User,
        related_name="posts_posted",
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        max_length=111,
    )
    text = models.CharField(
        max_length=555,
    )
    # Deprecated local image hosting
    # image = models.ImageField(upload_to="network/", blank=True)
    image = CloudinaryField("image")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner} posted {self.title}"


class PostForm(ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        exclude = ["owner"]
        widgets = {"text": forms.widgets.Textarea()}

    # No changes for now, later on this can change
    # If truly no changes, let's try using thet ModelForm Factory function


class Like(models.Model):
    post = models.ForeignKey(
        Post,
        related_name="likes",
        on_delete=models.CASCADE,
    )
    liker = models.ForeignKey(
        User,
        related_name="liked",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.post} is liked by {self.liker}"


class Follower(models.Model):
    following = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.CASCADE,
    )
    followed_by = models.ForeignKey(
        User,
        related_name="followed_by",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.followed_by} is following {self.following}"

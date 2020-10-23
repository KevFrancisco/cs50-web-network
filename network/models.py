from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm


class User(AbstractUser):
    pass

class Post(models.Model):
    owner = models.ForeignKey(
                        User,
                        related_name='posts_posted',
                        on_delete=models.CASCADE,
                    )
    text = models.CharField(
                        max_length=555,
                    )
    image = models.ImageField(
                        upload_to='network/',
                        blank=True
                    )
    timestamp = models.DateTimeField(
                        auto_now=True
                    )

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
    # No changes for now, later on this can change
    # If truly no changes, let's try using thet ModelForm Factory function

class Like(models.Model):
    post = models.ForeignKey(
                        Post,
                        related_name='likes',
                        on_delete=models.CASCADE,
                    )
    liker = models.ForeignKey(
                        User,
                        related_name='liked',
                        on_delete=models.CASCADE,
                    )

# FIXME is this model correct?
# We come back to this later quack
class Follower(models.Model):
    followed = models.ForeignKey(
                        User,
                        related_name='following',
                        on_delete=models.CASCADE,
                    )
    followed_by = models.ForeignKey(
                        User,
                        related_name='followed_by',
                        on_delete=models.CASCADE,
                    )
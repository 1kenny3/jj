from django.db import models

from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    rate = models.IntegerField()
    crated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField()
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    user = models.ForeignKey(
        User,
        models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-crated_at"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self) -> str:
        return f"{self.title} {self.pk}"

    def get_stars(self):
        return "⭐" * self.rate


class Comment(models.Model):
    content = models.CharField()
    create_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"

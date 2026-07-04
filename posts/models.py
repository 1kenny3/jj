from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    rate = models.IntegerField()
    crated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField()
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")

    class Meta:
        ordering = ["-crated_at"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self) -> str:
        return f"{self.title} {self.pk}"

    def get_stars(self):
        return "⭐" * self.rate


 
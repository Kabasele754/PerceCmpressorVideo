from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=100)
    original_file = models.FileField(upload_to='videos/')
    compressed_file = models.FileField(upload_to='compressed/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
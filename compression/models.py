from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/')
    output_file = models.FileField(upload_to='videos/compressed/', blank=True, null=True)
    compressed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

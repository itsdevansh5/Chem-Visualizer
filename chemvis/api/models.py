from django.db import models

# Create your models here.
class Dataset(models.Model):
    name = models.CharField(max_length=250)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/')
    summary = models.JSONField()  # stores total_count, averages, type_distribution
    preview_csv = models.TextField(blank=True)  # first rows for table display

    def __str__(self):
        return f"{self.name} ({self.uploaded_at})"
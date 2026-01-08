from django.db import models

# Create your models here.
class Audiogram(models.Model):
    original_file=models.ImageField(upload_to='audiograms/')
    filename=models.CharField(max_length=255)
    exam_date=models.DateField(null=True, blank=True)
    need_review=models.BooleanField(default=False)
    memo=models.TextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename


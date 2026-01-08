from django.db import models

# Create your models here.
class data(models.Model):
    original_file=models.ImageField()
    filname=models.CharField()
    exam_date=models.DateField()
    need_review=models.BooleanField()
    memo=models.TextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_created=True)

    def __str__(self):
        return data.filname


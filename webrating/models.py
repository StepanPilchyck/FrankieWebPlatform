from django.db import models

# Ckeditor support
from ckeditor.fields import RichTextField


class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=256)
    email = models.CharField(max_length=256, null=True, blank=True)
    comment = RichTextField()
    rating = models.FloatField()
    state = models.BooleanField(default=False)
    date_on_add = models.DateField(auto_now=True, blank=True)

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = 'ratings'
        verbose_name = 'Comment'
        verbose_name_plural = 'Ratings and comments'

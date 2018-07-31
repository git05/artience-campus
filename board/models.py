from django.db import models
from django_summernote import models as summer_model
from django_summernote import fields as summer_fields

class SummerNote(summer_model.Attachment):
    summer_field = summer_fields.SummernoteTextField(default='')
# Create your models here.

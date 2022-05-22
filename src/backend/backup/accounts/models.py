from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validate_company_id


class User(AbstractUser):
    website_url = models.URLField(blank=True)
    company_id = models.CharField(blank=True, max_length=12, validators=[validate_company_id])

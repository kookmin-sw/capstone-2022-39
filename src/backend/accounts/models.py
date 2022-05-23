from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from .validators import validate_company_id


class User(AbstractUser):
    phone_number = models.CharField(
        max_length=13,
        validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")],
        verbose_name='휴대폰 번호',
    )
    company_id = models.CharField(
        max_length=12,
        validators=[validate_company_id],
        verbose_name='사업자등록번호',
    )

    company_name = models.CharField(max_length=20, verbose_name='회사명')

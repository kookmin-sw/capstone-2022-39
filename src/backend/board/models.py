from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="작성자")
    title = models.CharField(
        max_length=20,
        validators=[MinLengthValidator(1), MaxLengthValidator(20)],
        verbose_name="제목"
    )
    url = models.URLField(blank=True, verbose_name="URL")
    location = models.CharField(max_length=50, verbose_name="근무지")
    gather_count = models.CharField(max_length=50, verbose_name="모집인원")
    category = models.CharField(max_length=10, verbose_name="모집분야")
    recruiter = models.CharField(max_length=50, verbose_name="담당자명", default='-')
    employment = models.CharField(max_length=70, verbose_name="고용형태", default='-')
    content = models.TextField(verbose_name="특이사항", default='-')
    pay = models.CharField(max_length=50, verbose_name="임금", default='-')
    work_time = models.CharField(max_length=50, verbose_name="근무시간", default='-')
    call_number = models.CharField(max_length=13, verbose_name="연락처", default='-')
    qualification_license = models.CharField(max_length=70, verbose_name="자격사항", default='-')

    def get_absolute_url(self):
        return reverse('board:post_detail', args=[self.pk])

    class Meta:
        ordering = ["-id"]

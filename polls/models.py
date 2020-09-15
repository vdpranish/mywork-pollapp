from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_recently_published(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_recently_published.admin_order_field = 'pub_date'
    was_recently_published.boolean = True
    was_recently_published.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    vote = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class UserProfileImg(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_pic', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    USER = 'user'
    ADMIN = 'admin'
    user_option = [
        (USER, 'USER'),
        (ADMIN, 'ADMIN')
    ]
    role = models.CharField(max_length=5, choices=user_option, default=USER, blank=True,null=True)

    def __str__(self):
        return f'{self.user.username} Role'


class UploadPdf(models.Model):
    pdf_name = models.CharField(max_length=100, blank=True)
    pdf_file = models.FileField(upload_to='pdf')

    def __str__(self):
        return self.pdf_name

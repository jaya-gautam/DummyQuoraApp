from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Writer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_id = models.EmailField(max_length=70, blank=True)
    created_date = models.DateField(null=True, default=timezone.now())
    credit_points = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return self.user.username



class Question(models.Model):
    writer = models.ForeignKey(Writer, on_delete=models.SET_NULL, null=True)
    question_body = models.TextField(max_length=1000, help_text='Enter your question in brief')
    created_date = models.DateField(null=True, default=timezone.now())
    updated_date = models.DateField(null=True, default=timezone.now())

    def get_absolute_url(self):
        return reverse('question-detail', args=[str(self.id)])

    def __str__(self):
        return self.question_body


class Answer(models.Model):
    writer = models.ForeignKey(Writer, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey('Question', on_delete=models.SET_NULL, null=True)
    answer_body = models.TextField(max_length=2000, help_text='Write your answer here...')
    created_date = models.DateField(null=True, default=timezone.now())
    updated_date = models.DateField(null=True, default=timezone.now())
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    def __str__(self):
        return f'Que: {self.question.question_text[:50]}.. Ans: {self.answer_text[:50]}..'


class Comment(models.Model):
    writer = models.ForeignKey(Writer, on_delete=models.SET_NULL, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True)
    comment_body = models.TextField(max_length=1000, help_text='Enter your comment...')
    created_date = models.DateField(default=timezone.now())
    updated_date = models.DateField(default=timezone.now())

    def __str__(self):
        return self.comment_body




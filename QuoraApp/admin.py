from django.contrib import admin
from QuoraApp.models import *


# Register your models here.

class WriterAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_date', 'credit_points')
admin.site.register(Writer, WriterAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_body', 'created_date')
    list_filter = ('created_date', )
admin.site.register(Question, QuestionAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'question', 'answer_body', 'writer', 'created_date', 'upvote', 'downvote', 'views')
    list_filter = ('created_date', 'writer', 'upvote', 'downvote', 'views')
    fieldsets = (
        (None, {
            'fields': ('writer','question', 'answer_text')
        }),
        ('Dates', {
            'fields': ('created_date', 'updated_date')
        }),
        ('Actions', {
            'fields': ('upvote', 'downvote', 'views')
        }),
    )

admin.site.register(Answer, AnswerAdmin)



class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_body',  'created_date')
admin.site.register(Comment, CommentAdmin)

"""QuoraProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from QuoraApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('question/add/', views.QuestionCreateView.as_view(), name='question-add'),
    path('questions/', views.QuestionList.as_view(), name='questions'),
    path('answers/', views.AnswerList.as_view(), name='answers'),
    path('question/<int:pk>', views.QuestionDetailView.as_view(), name='question-detail'),
    path('question/<int:pk>/answer/', views.AnswerCreateView.as_view(), name='answer-add'),
    path('question/<int:pk>/update/', views.UpdateQuestionView.as_view(), name='question-update'),
    path('answer/<int:pk>/update/', views.UpdateAnswerView.as_view(), name='answer-update'),
    path('answer/<int:pk>/comment/', views.CommentCreateView.as_view(), name='comment-add'),
    path('answer/upvote/<int:pk>', views.UpvoteCreateView.as_view(), name='answer-upvote'),
    path('answer/downvote/<int:pk>', views.DownvoteCreateView.as_view(), name='answer-downvote'),
    path('author/<int:pk>', views.WriterDetailView.as_view(), name='author-detail'),
    path('author/add/', views.WriterCreateView.as_view(), name='author-add'),
    path('author/<int:pk>/', views.WriterUpdateView.as_view(), name='author-update'),
    path('', RedirectView.as_view(url='/QuoraApp/')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

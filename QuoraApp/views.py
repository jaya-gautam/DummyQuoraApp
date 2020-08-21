from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from QuoraApp.models import *



class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['question_body', 'credit_points']

    def get(self, request, *args, **kwargs):
        return render(request, 'question_form.html')

    def post(self, request, *args, **kwargs):
        question_body = request.POST.get('question_text')
        print(self.request.user)
        Question.objects.create(writer=Writer.objects.get(user=self.request.user), question_body = question_body)
        response = redirect('questions')
        return response


class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    fields = ['answer_body']

    def get(self, request, *args, **kwargs):
        q_id = self.kwargs['pk']
        return render(request, 'answer_form.html', {"q_id": q_id})

    def post(self, request, *args, **kwargs):
        answer_body = request.POST.get('answer_text')
        answer = Answer.objects.create(writer=Writer.objects.get(
            user=self.request.user), question=Question.objects.get(
                id=self.kwargs['pk']), answer_body=answer_body)
        response = redirect(reverse('question-detail', kwargs={'pk': answer.question.id}))
        return response


class WriterCreateView(CreateView):
    model = Writer
    fields = ['email_id', 'credit_points']

    def get(self, request, *args, **kwargs):
        return render(request, 'writer_form.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email_id = request.POST.get('email')

        if password1 == password2:
            hasher = PBKDF2PasswordHasher()
            password = hasher.encode(
                password=password1, salt='salt', iterations=150000)

            user = User.objects.create(username=username, password=password)
            Writer.objects.create(user=user, email_id=email_id, )
            response = redirect('/accounts/login/')
            print('match pass')
            return response
        else:
            print('else')
            return render(request, 'writer_form.html')


class UpdateAnswerView(LoginRequiredMixin, UpdateView):
    model = Answer
    fields = ['answer_body']
    template_name = 'answer_update_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answer_id = self.kwargs['pk']
        answer = Answer.objects.get(id=answer_id)
        self.pk = answer.question.id
        context['answer_body'] = answer.answer_body
        return context

    def get_success_url(self):
        return (reverse('question-detail', kwargs={'pk': self.object.question.id}))


class UpdateQuestionView(LoginRequiredMixin, UpdateView):
    model = Question
    fields = ['question_body']
    success_url = reverse_lazy('questions')
    template_name = 'question_update_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_id = self.kwargs['pk']
        question = Question.objects.get(id=question_id)
        context['question_text'] = question.question_body
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['writer', 'answer', 'comment_body']

    def get(self, request, *args, **kwargs):
        a_id = self.kwargs['pk']
        return render(request, 'comment_form.html', {"a_id": a_id})

    def post(self, request, *args, **kwargs):
        comment_text = request.POST.get('comment_text')
        params = self.kwargs['pk']
        writer = Writer.objects.get(user=self.request.user)
        answer = Answer.objects.get(id=params)
        Comment.objects.create(
            writer=writer, answer=answer, comment_body=comment_text)
        response = redirect(
            reverse('question-detail', kwargs={'pk': answer.question.id}))
        return response


class UpvoteCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    fields = ['answer_body', 'id', 'upvote']

    def post(self, request, *args, **kwargs):
        answer_id = self.kwargs['pk']
        answer = Answer.objects.get(id=answer_id)
        answer.upvote += 1
        answer.save()
        response = redirect(
            reverse('question-detail', kwargs={'pk': answer.question.id}))
        return response


class DownvoteCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    fields = ['answer_body', 'id', 'downvote']

    def post(self, request, *args, **kwargs):
        answer_id = self.kwargs['pk']
        answer = Answer.objects.get(id=answer_id)
        answer.downvote += 1
        answer.save()
        response = redirect(
            reverse('question-detail', kwargs={'pk': answer.question.id}))
        return response





class WriterUpdateView(UpdateView):
    model = Writer
    fields = ['email_id']


class WriterDeleteView(DeleteView):
    model = Writer
    fields = ['user']
    fields = ['email_id']
    fields = ['credit_points']
    success_url = reverse_lazy('questions')


class WriterDetailView(generic.DetailView):
    model = Writer


class QuestionDetailView(generic.DetailView):
    """Generic class-based detail view for a Question."""
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_id = self.kwargs['pk']
        question = Question.objects.get(id=question_id)
        answer_list = Answer.objects.filter(question=question)
        comment_dictionary = {
                ans.id: Comment.objects.filter(answer=ans) for ans in answer_list
            }
        context['answer_list'] = answer_list
        context['answer_url'] = '/question/'+str(question_id)+'/answer/'
        context['upvote_url'] = '/answer/upvote/'
        context['downvote_url'] = '/answer/downvote/'
        context['comment_dictionary'] = comment_dictionary
        return context


class AnswerList(generic.ListView):
    model = Answer
    paginate_by = 3


class QuestionList(generic.ListView):
    model = Question
    paginate_by = 10
    queryset = Question.objects.all()


def index(request):
    num_questions = Question.objects.all().count()
    num_answers = Answer.objects.all().count()
    num_writers = Writer.objects.count()
    num_comments = Comment.objects.count()
    context = {
        'num_questions': num_questions,
        'num_answers': num_answers,
        'num_writers': num_writers,
        'num_comments': num_comments,
    }
    return render(request, 'index.html', context=context)


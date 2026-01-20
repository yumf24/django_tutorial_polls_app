from datetime import time
from django.utils import timezone
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import re
from .models import Question, Choice
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "question_latest"

    def get_queryset(self):
        return (Question.objects.filter(pub_time__lte = timezone.now()).order_by("-pub_time")[:5]) 

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        return Question.objects.filter(pub_time__lte = timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {"question":question, "err_message":"You have not select the choice"})
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))

""" old views

def index(request):
    question_latest = Question.objects.order_by("-pub_time")[:5]
    context = {"question_latest":question_latest}
    return render(request, "polls/index.html", context)

def polls_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question":question})



def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question":question})

"""

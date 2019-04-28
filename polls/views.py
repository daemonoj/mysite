from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.template import loader
from django.utils import timezone

from .models import Choice, Question



class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def create_poll(request):
	template = loader.get_template('polls/createpoll.html')
	return HttpResponse(template.render({'key':''},request))

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        print (request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def add_question(request):
	question = Question(question_text=request.POST['question'], pub_date=timezone.now())
	question.save()
	question.choice_set.create(choice_text=request.POST['choice1'],votes=0)
	question.choice_set.create(choice_text=request.POST['choice2'],votes=0)
	return HttpResponseRedirect(reverse('polls:detail',args=(question.id,)))
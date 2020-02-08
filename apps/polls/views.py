# Create your views here.
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView

from apps.polls.models import Question, Choice


class IndexView(ListView):
    # Django CBV
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

# # Orientado à função
# def index(request):
#     """ :returns last 5 Questions objects
#         filter by pub_date
#     """
#
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list': latest_question_list
#     }
#     return render(request, 'polls/index.html', context)


class DetailView(DetailView):
    # Django CBV
    model = Question
    template_name = 'polls/detail.html'

# # Orientado à função
# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # return render(request, 'polls/detail.html', {'question': question})
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})


class ResultsView(DetailView):
    model = Question
    template_name = 'polls/results.html'

# # Orientado à função
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})


# # Orientado à função
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1

        # O código da nossa view vote() tem um pequeno problema. Ele primeiro pega o
        # objeto de selected_choice do banco de dados, calcula o novo valor de votes
        # e os salva novamente. Se dois usuários do seu site tentarem votar ao mesmo
        # tempo: o mesmo valor, digamos 42, será obtido para votes. Então, para ambos
        # usuários, o novo valor 43 é calculado e salvo, quando o valor esperado
        # seria 44. Isto é chamado de condição de concorrência. Se você estiver
        # interessado, pode ler Avoiding race conditions using F() para aprender como
        # resolver este problema:
        # selected_choice.votes = F('votes')+1

        # ou, reduzindo querys sem precisar do get() e save()
        # selected_choice.update(votes=F('votes') + 1)

        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
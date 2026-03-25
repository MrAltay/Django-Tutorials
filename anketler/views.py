from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question, Poll


class IndexView(generic.ListView):
    template_name = "anketler/index.html"
    context_object_name = "latest_poll_list"

    def get_queryset(self):
        """
        Return the last ten published polls (not including those set to be
        published in the future).
        """
        return Poll.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:10]


class DetailView(generic.DetailView):
    model = Poll
    template_name = "anketler/detail.html"
    
    def get_queryset(self):
        """
        Excludes any polls that aren't published yet.
        """
        return Poll.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Poll
    template_name = "anketler/results.html"


def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    
    # Process votes for multiple questions
    votes_saved = 0
    for question in poll.question_set.all():
        choice_id = request.POST.get(f"question_{question.id}")
        if choice_id:
            try:
                selected_choice = question.choice_set.get(pk=choice_id)
                selected_choice.votes = F("votes") + 1
                selected_choice.save()
                votes_saved += 1
            except (ValueError, Choice.DoesNotExist):
                pass

    if votes_saved == 0:
        # Redisplay the poll voting form if no choice is selected at all
        return render(
            request,
            "anketler/detail.html",
            {
                "poll": poll,
                "error_message": "Lütfen en az bir soru için seçim yapın.",
            },
        )
    return HttpResponseRedirect(reverse("anketler:results", args=(poll.id,)))

def create_poll(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if not title:
            return HttpResponseRedirect(reverse("anketler:index"))
        
        poll = Poll.objects.create(title=title, pub_date=timezone.now())
        
        # Parse dynamic question and choice fields
        q_index = 0
        while f"q_{q_index}_text" in request.POST:
            q_text = request.POST[f"q_{q_index}_text"].strip()
            if q_text:
                question = Question.objects.create(poll=poll, question_text=q_text)
                
                c_index = 0
                while f"q_{q_index}_c_{c_index}" in request.POST:
                    c_text = request.POST[f"q_{q_index}_c_{c_index}"].strip()
                    if c_text:
                        Choice.objects.create(question=question, choice_text=c_text, votes=0)
                    c_index += 1
            q_index += 1
            
        return HttpResponseRedirect(reverse("anketler:index"))
    
    return HttpResponseRedirect(reverse("anketler:index"))

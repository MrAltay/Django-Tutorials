import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anket_sistemi.settings')
django.setup()

from django.contrib.auth.models import User
from anketler.models import Poll, Question, Choice

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')

# Create Poll
p = Poll.objects.create(title="Sivas Anketi", pub_date=timezone.now())

# Create Questions
q1 = Question.objects.create(poll=p, question_text="Sivas'ın en meşhur yemeği nedir?")
Choice.objects.create(question=q1, choice_text="Sivas Köftesi", votes=0)
Choice.objects.create(question=q1, choice_text="Hingel", votes=0)
Choice.objects.create(question=q1, choice_text="Madımak", votes=0)

q2 = Question.objects.create(poll=p, question_text="Sivas'ın en turistik yeri neresidir?")
Choice.objects.create(question=q2, choice_text="Divriği Ulu Camii", votes=0)
Choice.objects.create(question=q2, choice_text="Gök Medrese", votes=0)
Choice.objects.create(question=q2, choice_text="Buruciye Medresesi", votes=0)

print("Database populated successfully.")

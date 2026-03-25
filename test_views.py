import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anket_sistemi.settings')
django.setup()

from django.test import Client
c = Client(SERVER_NAME='localhost')

print("Testing Create Poll...")
resp = c.post('/anketler/create/', {
    'title': 'Test Yeni Anket',
    'q_0_text': 'Yeni Soru 1?',
    'q_0_c_0': 'Cevap 1',
    'q_0_c_1': 'Cevap 2',
    'q_1_text': 'Yeni Soru 2?',
    'q_1_c_0': 'Cevap A',
    'q_1_c_1': 'Cevap B'
})

assert resp.status_code == 302, f"Create poll failed to redirect with status {resp.status_code}"

from anketler.models import Poll
new_poll = Poll.objects.get(title='Test Yeni Anket')
assert new_poll.question_set.count() == 2, "Questions not created correctly"
q1 = new_poll.question_set.first()
assert q1.choice_set.count() == 2, "Choices not created correctly"

print("All tests passed successfully!")

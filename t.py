from datetime import datetime
from django.utils import timezone

print(timezone.make_naive(datetime.now()) )
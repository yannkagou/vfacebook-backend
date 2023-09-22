# -*- coding: utf-8 -*-

import django
import os
import sys

from datetime import timedelta
from collections import Counter
from django.utils import timezone


sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from post.models import Post, Trend

def extract_hashtag(text, trends):
    for word in text.split():
        if word[0] =='#':
            trends.append(word[1:])
    
    return trends

for trend in Trend.objects.all():
    trend.delete()

trends = []

this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
twenty_four_hours = this_hour - timedelta(hours=24)

for post in Post.objects.filter(created_at__gte=twenty_four_hours):
    extract_hashtag(post.body, trends)

# print(Counter(trends))

trends_counter = Counter(trends)

for trend in trends_counter:
    # print(trend[0], trend[1])
    Trend.objects.create(hashtag=trend[0], occurences=trend[1])
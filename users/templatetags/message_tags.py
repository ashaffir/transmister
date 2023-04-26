from django import template
from django.contrib.messages.storage.fallback import FallbackStorage

register = template.Library()


@register.filter
def most_recent_message(messages):
    return messages and messages[-1] or None

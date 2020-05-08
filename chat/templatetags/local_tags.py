from django import template
from ..models import Message
from django.db.models import Q

register = template.Library()

@register.filter
def last_message(user1, user2):
	message = Message.objects.filter(
		Q(
			Q(source=user1, destination=user2) |
			Q(source=user2, destination=user1)
		)
	).last()

	return "" if not message else f"{message.source.user.first_name}:{message.content}"

@register.filter
def last_message_time(user1, user2):
	message = Message.objects.filter(
		Q(
			Q(source=user1, destination=user2) |
			Q(source=user2, destination=user1)
		)
	).last()
	return "" if not message else f"{message.timestamp.hour}:{message.timestamp.minute}"

@register.filter
def unread_messages(user1, user2):
	messages = Message.objects.filter(
		source=user1 , destination=user2, read=False
	)
	return messages.count()
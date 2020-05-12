from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from django.shortcuts import render
from django.db.models import F, Count
from django.contrib.auth.models import Group

from datetime import date, timedelta, datetime

from .models import *
from .serializers import *

class MessageViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Message.objects.all()
	serializer_class = MessageSerializer

	# def create(self, request, *args, **kwargs):
	# 	print(request.POST)
	# 	super(MessageViewset, self).create(request, *args, **kwargs)

	# @action(methods=['GET'], detail=False, url_name="chart_mode",
	# 	url_path=r'modedu(?P<debut>(\d{1,4}[-]?){3})au(?P<fin>(\d{1,4}[-]?){3})', )
	# def modedetail(self, request, debut, fin):
	# 	fin = datetime.strptime(fin, "%Y-%m-%d")
	# 	debut = datetime.strptime(debut, "%Y-%m-%d")
	# 	data = []
	# 	mode = Panier.objects\
	# 		.filter(commande__date__lte=fin, commande__date__gte=debut)\
	# 		.values('recette__nom').annotate(times=Count('recette__nom'))

	# 	return Response({
	# 		'labels': [panier['recette__nom'] for panier in mode],
	# 		"datasets":[
	# 			{'data':[panier['times'] for panier in mode]},
	# 		]})

class ContactViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Contact.objects.all()
	serializer_class = ContactSerializer

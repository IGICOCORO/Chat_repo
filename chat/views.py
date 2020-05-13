from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.models import User
from django.db.models import Q

from .models import *
from .serializers import *
from .forms import *

class Home(View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_initial = request.user.username[0].upper()
            contacts = Contact.objects.all()
            return render(request, self.template_name, locals())
        else:
            return redirect("login")

def disconnect(request):
    show_hidden = "hidden"
    logout(request)
    return redirect("login")


class Connexion(View):
    template_name = "login.html"
    next_p = "home"

    def get(self, request, *args, **kwargs):
        form = ConnexionForm()
        try:
            self.next_p = request.GET["next"]
        except:
            print
        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)
                messages.success(request, "You're now connected!")
                return redirect(self.next_p)
            else:
                messages.error(request, "logins incorrect!")
        return render(request, self.template_name, locals())

class Chat(View):
    template_name = 'chat.html'
    next_p = "home"

    def get(self, request, id_user, *args, **kwargs):
        form = MessageForm()
        contacts = Contact.objects.all()
        user_initial = request.user.username[0].upper()
        source = Contact.objects.get(user = request.user)
        destination = Contact.objects.get(user=id_user)
        Message.objects\
            .filter(Q(source=destination, destination=source))\
            .update(read=True)
        messages =  Message.objects.filter(
                Q(
                    Q(source=source, destination=destination) |
                    Q(source=destination, destination=source)
                )
            ).order_by("timestamp")
        return render(request, self.template_name, locals())

    def post(self, request, id_user, *args, **kwargs):
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            source = Contact.objects.get(user = request.user)
            destination = Contact.objects.get(user=id_user)
            message.source = source
            message.destination = destination
            message.save()
            messages = Message.objects.filter(
                Q(
                    Q(source=source, destination=destination) |
                    Q(source=destination, destination=source)
                )
            ).order_by("timestamp")
        return render(request, self.template_name, locals())

class Register(View):
    template_name = 'register.html'
    next_p = "home"

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        try:
            self.next_p = request.GET["next"]
        except:
            print
        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                firstname = form.cleaned_data['firstname']
                lastname = form.cleaned_data['lastname']
                password = form.cleaned_data['password']
                picture = form.cleaned_data['picture']
                user = User.objects.create_user(
                    username=username,
                    password=password)
                user.first_name, user.last_name = firstname, lastname
                user.save()
                Contact(user=user, picture=picture).save()
                messages.success(request, "Hello "+username+", youn are registered successfully!")
                if user:
                    login(request, user)
                    return redirect("home")
            except Exception as e:
                print(str(e))
                messages.error(request, str(e))
        return render(request, self.template_name, locals())




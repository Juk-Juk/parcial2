from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistroForm

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Save the form to create the user
            user = form.save()

            # Send a welcome email
            subject = '¡Bienvenido a nuestro sitio web!'
            message = f'Hola {user.username},\n\nGracias por registrarte en nuestro sitio web.\n\n¡Disfruta de tu experiencia!'
            from_email = settings.EMAIL_HOST_USER  # Use the email from settings
            recipient_list = [user.email]  # Send to the new user's email

            # Send the email
            send_mail(subject, message, from_email, recipient_list)

            # Redirect the user to the login page after registration
            return redirect('cuentas:login')
    else:
        form = RegistroForm()
    
    return render(request, 'registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('cuentas:login')

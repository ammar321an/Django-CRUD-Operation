from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from .models import RegistrationForm
from .forms import RegistrationFormForm
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.contrib.auth import authenticate, login
import json

def home(request):
    return render(request, 'AiApp/home.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('retype_password')

        if RegistrationForm.objects.filter(email=email).exists():
            return HttpResponse("Email already exists")

        if len(password) < 8:
            return HttpResponse("Password must be at least 8 characters long")

        if password != repassword:
            return HttpResponse("Passwords do not match")

        hashed_password = make_password(password)

        user = User.objects.create(
            username=name,
            email=email,
            password=hashed_password,
            last_login=timezone.now(),
            date_joined=timezone.now(),
        )

        RegistrationForm.objects.create(
            user=user,
            name=name,
            email=email,
            password=hashed_password,
            repassword=hashed_password,
            date_reg=timezone.now(),
        )

        session_key = Session.objects.create(
            session_key=user.username,
            session_data='',
            expire_date=timezone.now() + timezone.timedelta(minutes=20),
        )

        return redirect('authenticate_email')

    return render(request, 'AiApp/register.html')


def dashboard(request):
    return render(request, 'AiApp/dashboard.html')


# def database(request):
#     return render(request, 'AiApp/database.html')

def authenticate_email(request):
    #just simulate success
    return render(request, 'AiApp/authenticate_email.html')

def check_email(request):
    email = request.GET.get('email', None)
    if email is None:
        return JsonResponse({'error': 'Email parameter missing'}, status=400)
    
    data = {
        'is_taken': User.objects.filter(username=email).exists()
    }
    return JsonResponse(data)

def insert_database(request):
    if request.method == 'POST':
        form = RegistrationFormForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(username=email).exists():
                messages.error(request, 'This email is already registered.')
            else:
                user = User(username=email, email=email)
                user.set_password(form.cleaned_data['password'])
                user.save()

                registration_form = RegistrationForm(
                    user=user,
                    name=form.cleaned_data['name'],
                    email=email,
                    password=user.password,  # Save the hashed password
                    repassword=user.password,
                    date_reg=timezone.now()
                )
                registration_form.save()
                messages.success(request, 'Registration successful!')
                form = RegistrationFormForm()  # Reset the form
    else:
        form = RegistrationFormForm()
    
    # Fetch all records
    registration_forms = RegistrationForm.objects.all()
    
    return render(request, 'AiApp/insert_database.html', {'form': form, 'registration_forms': registration_forms})

def delete_registration(request, pk):
    if request.method == 'POST':
        try:
            registration_form = RegistrationForm.objects.get(pk=pk)
            user = registration_form.user  # Get the associated User

            # Delete the registration form and the user
            registration_form.delete()
            user.delete()

            return JsonResponse({'status': 'success', 'message': 'Registration deleted successfully.'}, status=200)
        except RegistrationForm.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Registration not found.'}, status=404)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)

def update_registration(request, pk):
    if request.method == 'POST':
        try:
            registration_form = RegistrationForm.objects.get(user_id=pk)
            name = request.POST.get('name')
            email = request.POST.get('email')

            if name:
                registration_form.name = name
            if email:
                registration_form.email = email

            registration_form.save()
            return JsonResponse({'status': 'success', 'message': 'Registration updated successfully.'}, status=200)
        except RegistrationForm.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User ID not found.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)

def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        try:
            user = User.objects.get(email=email)
            auth_user = authenticate(request, username=user.username, password=password)
            
            if auth_user is not None:
                login(request, auth_user)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'wrong_password'})
        
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'email_not_exist'})

    return render(request, 'AiApp/login.html')
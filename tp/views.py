from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import google.generativeai as genai
from django.conf import settings
from tp.models import register as re , Script
from tp.forms import regform,forgotform,passform,Script
from django.contrib.auth.views import PasswordResetView
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import check_password ,make_password
# Create your views here.


def index(request):
    return render(request,'index.html')
def skill(request):
    return render(request,'skill.html')
def educ(request):
    return render(request,'educ.html')
def activ(request):
    return render(request,'activ.html')
def login(request):
    return render(request,'login.html')
def verify(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user1 = re.objects.get(Email=email)
        except re.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
        except Exception as e:
            print(e)
            return render(request, 'login.html', {'error': 'An unexpected error occurred'})

        
        if check_password(password, user1.password):
            
            return redirect('home')  
        else:
            
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    else:
        
        return render(request, 'login.html')

def register(request):
    if request.method=='POST':
        fm=regform(request.POST)
        if fm.is_valid():
            password=fm.cleaned_data['password']
            hashed_password=make_password(password)
            new_user=fm.save(commit=False)
            new_user.password=hashed_password
            new_user.save()
            return redirect('login')
    else:
        fm = regform()
      
    return render(request,'register.html',{'register': fm}) 
def password(request):
    return render(request,'password.html')
def password_reset_email(request):
    return render(request,'password_reset_email.html')  

@login_required
def home(request):
    user = request.user
    if user.is_authenticated:
        full_name = f'{user.first_name} {user.last_name}'.strip()
        if not full_name:
            full_name = user.username  # Or user.get_full_name() if available
        profile_picture = user.socialaccount_set.filter(provider='google').first().extra_data.get('picture', '')

        context = {'full_name': full_name, 'profile_picture': profile_picture}
    return render(request, 'home.html', context)

def forgot(request):
    if request.method == 'POST':
        form = forgotform(request.POST)
        if form.is_valid():
            email = form.cleaned_data['Email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return render(request, 'forgot.html', {'error': 'Invalid email address'})
            
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            current_site = get_current_site(request)
            protocol = 'http' if not request.is_secure() else 'https'
            reset_url = f"{protocol}://{current_site.domain}{reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"
            mail_subject = 'Reset your password'
            context = {
                'reset_url': reset_url
            }
            html_message = render_to_string('password.html', context)
            text_message = strip_tags(html_message)
            email = EmailMultiAlternatives(
                subject=mail_subject,
                body=text_message,
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email],
            )
            email.attach_alternative(html_message, "text/html")  # Attach HTML content
            email.send()
            
            return render(request,'password_reset_email.html',{'sent':'email sent'})
    
    else:
        form = forgotform()
    return render(request, 'forgot.html', {'form': form})

     




def answer(request):
    user = request.user
    full_name = f'{user.first_name} {user.last_name}'.strip() or user.username
    profile_picture = user.socialaccount_set.filter(provider='google').first().extra_data.get('picture', '')
    if request.method == 'POST':
        question = request.POST.get('question')
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 8192,
        }

        safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        } ,
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

        convo = model.start_chat(history=[
        {
            "role": "user",
            "parts": [question]
        }
        ])

        convo.send_message(content=question)
        while not convo.last.text:
            pass

        response = convo.last.text
    

        context = {
            'question': question,
            'response': response,
            'full_name': full_name,
            'profile_picture': profile_picture
        }
        return render(request, 'answer.html', context)

    else:
        return render(request, 'answer.html', {
            'full_name': full_name,
            'profile_picture': profile_picture
        })

    
def submit_script(request):
    if request.method == 'POST':
        form = NewScriptForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Replace 'success_page' with your actual URL name
    else:
        form = NewScriptForm()
    

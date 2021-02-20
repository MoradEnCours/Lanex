from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from lanex.models import Language, LanguageRequest
from lanex.forms import LanguageForm, RequestForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request):
    language_list = Language.objects.order_by('-likes')[:5]
    request_list = LanguageRequest.objects.order_by('-views')[:5]
    context_dict = {}
    context_dict['boldmessage'] = 'filler text to be replaced'
    context_dict['languages'] = language_list
    context_dict['requests'] = request_list
    visitor_cookie_handler(request)
    return render(request, 'lanex/index.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage': 'A bit of tinkering and testing going on here'}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    return render(request, 'lanex/about.html', context=context_dict)

def explore(request):
    language_list = Language.objects.all()[:5]
    request_list = LanguageRequest.objects.order_by('-views')[:5]
    context_dict = {}
    context_dict['languages'] = language_list
    context_dict['requests'] = request_list
    return render(request, 'lanex/explore.html', context=context_dict)

def languages(request):
    language_list = Language.objects.all()[:5]
    context_dict = {}
    context_dict['languages'] = language_list
    return render(request, 'lanex/languages.html', context=context_dict)

def show_language(request, language_name_slug):
    context_dict = {}
    try:
        language = Language.objects.get(slug=language_name_slug)
        requests = LanguageRequest.objects.filter(language=language)
        context_dict['requests'] = requests
        context_dict['language'] = language
    except Language.DoesNotExist:
        context_dict['language'] = None
        context_dict['requests'] = None
    return render(request, 'lanex/language.html', context=context_dict)


@login_required
def add_language(request):
    if request.user.is_superuser:
        form = LanguageForm()
    
        if request.method == 'POST':
            form = LanguageForm(request.POST)
            if form.is_valid():
                form.save(commit=True)
                return redirect('/')
            else:
                print(form.errors)
    
        return render(request, 'lanex/add_language.html', {'form': form})
    
    else:
        return redirect('/')

### Come back to this later, incomplete
'''
@login_required
def add_language_request(request, language_name_slug):
    try:
        language = Language.objects.get(slug=language_name_slug)
    except Language.DoesNotExist:
        language = None
    
    if language is None:
        return redirect('/')
    
    form = LanguageRequestForm()
    
    if request.method == 'POST':
        form = LanguageRequestForm(request.POST)
    
        if form.is_valid():
            if language:
                lang_request = form.save(commit=False)
                lang_request.language = language
                lang_request.views = 0
                lang_request.creator = request.user
    
                if 'picture' in request.FILES:
                    lang_request.picture = request.FILES['picture']
    
                lang_request.completed = False
                lang_request.save()
                return redirect(reverse('lanex:show_request',
                                         kwargs={'language_name_slug': language_name_slug, 
                                        'request_name_slug': lang_request.request_id}))
        else:
            print(form.errors)
    
    context_dict = {'form': form, 'language': language}
    return render(request, 'lanex/add_request.html', context=context_dict)
'''

@login_required
def add_request(request):
    form = RequestForm()
    
    if request.method == 'POST':
        form = RequestForm(request.POST)
    
        if form.is_valid():
            lang_request = form.save(commit=False)
            lang_request.views = 0
            lang_request.creator = request.user
    
            if 'picture' in request.FILES:
                    lang_request.picture = request.FILES['picture']
    
            lang_request.completed = False
            lang_request.save()
            return redirect(reverse('lanex:show_request', 
                                    kwargs={'language_name_slug': lang_request.language, 
                                    'request_name_slug': lang_request.request_id}))
    
        else:
            print(form.errors)

    context_dict = {'form': form}
    return render(request, 'lanex/add_request.html', context=context_dict)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'lanex/register.html', 
                            context={'user_form': user_form, 
                                    'profile_form': profile_form, 
                                    'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('lanex:index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'lanex/login.html')


@login_required
def restricted(request):
    return render(request, 'lanex/restricted.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('lanex:index'))


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits+1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits



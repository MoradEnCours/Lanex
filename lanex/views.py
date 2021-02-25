from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse
from lanex.models import Language, LanguageRequest, UserProfile
from lanex.forms import LanguageForm, RequestForm, UserForm, UserProfileForm, UserForm2
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    if request.user.is_authenticated:
        if timezone.now() - request.user.date_joined < timedelta(seconds=5):
            return redirect(reverse('lanex:user_settings', 
                                    kwargs={'user_profile_slug': request.user}))

    language_list = Language.objects.all()[:5]
    request_list = LanguageRequest.objects.order_by('-views')[:5]
    context_dict = {}
    context_dict['languages'] = language_list
    context_dict['requests'] = request_list
    return render(request, 'lanex/index.html', context=context_dict)



def about(request):
    context_dict = {}
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


def show_request(request, language_name_slug, request_name_slug):
    context_dict = {}
    
    try:
        lang_request = LanguageRequest.objects.get(slug=request_name_slug)
        LanguageRequest.objects.filter(slug=request_name_slug).update(views=lang_request.views+1)
        context_dict['request'] = lang_request
        comments = lang_request.comments.filter(active=True)
        new_comment = None
        
        # Comment posted
        if request.method == 'POST':
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.creator = request.user
                new_comment.request = lang_request
                new_comment.save()
                context_dict['new_comment'] = new_comment
            else:
                comment_form = CommentForm()
                context_dict['comment_form'] = comment_form
            
            context_dict['comment_form'] = comment_form
        context_dict['comments'] = comments
    
    except LanguageRequest.DoesNotExist:
        context_dict['request'] = None
    
    return render(request, 'lanex/request.html', context=context_dict)


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


def show_user(request, user_profile_slug):
    context_dict = {}
    try:
        user = User.objects.get(username=user_profile_slug)
        user_profile = UserProfile.objects.get(user=user)
        context_dict['user_profile'] = user_profile
        
        try:
            user_requests = LanguageRequest.objects.filter(creator=user)
            context_dict['requests'] = user_requests
        except LanguageRequest.DoesNotExist:
            context_dict['requests'] = None
    
    except User.DoesNotExist:
        context_dict['user_profile'] = None
    
    return render(request, 'lanex/user.html', context=context_dict)



def search(request):
    query = request.GET.get('q')
    request_list = None
    
    if query != None:
        request_list = LanguageRequest.objects.filter(Q(title__icontains=query) | Q(desc__icontains=query)) 
        return render(request, 'lanex/search.html', {'query': query,'requests': request_list}) 
    
    return render(request, 'lanex/search.html', {'query': query, 'requests': request_list})


@login_required
def accept_request(request, language_name_slug, request_name_slug):
    lang_request = LanguageRequest.objects.get(slug=request_name_slug)
    if lang_request.creator != request.user:
        LanguageRequest.objects.filter(slug=request_name_slug).update(completed=True)
        return redirect(reverse('lanex:show_user', 
                                kwargs={'user_profile_slug': lang_request.creator.username}))
    else:
        return redirect(reverse('lanex:show_request', 
                                kwargs={'language_name_slug': lang_request.language, 
                                        'request_name_slug': lang_request.request_id}))



@login_required
def delete_request(request, language_name_slug, request_name_slug):
    lang_request = LanguageRequest.objects.get(slug=request_name_slug)
    if lang_request.creator == request.user:
        LanguageRequest.objects.filter(slug=request_name_slug).delete()
        return redirect(reverse('lanex:show_user', 
                            kwargs={'user_profile_slug': lang_request.creator.username}))
    else:
        return redirect(reverse('lanex:show_request', 
                            kwargs={'language_name_slug': lang_request.language, 
                                    'request_name_slug': lang_request.request_id}))


@login_required
def user_settings(request, user_profile_slug):
    if user_profile_slug == request.user.username:
        user_profile = UserProfile.objects.get(user=request.user)
        
        if request.method == "POST":
            update_user_form = UserForm2(data=request.POST, instance=request.user)
            update_profile_form = UserProfileForm(data=request.POST, instance=user_profile)
        
            if update_user_form.is_valid() and update_profile_form.is_valid():
                user = update_user_form.save()
                profile = update_profile_form.save(commit=False)
                profile.user = user
        
                if 'picture' in request.FILES:
                    profile.picture = request.FILES['picture']
        
                profile.save()
                return redirect(reverse('lanex:show_user', 
                                        kwargs={'user_profile_slug': user_profile_slug}))
            else:
                print(update_user_form.errors, update_profile_form.errors)
        
        else:
            update_user_form = UserForm2(instance=request.user)
            update_profile_form = UserProfileForm(instance=user_profile)
        return render(request, 'lanex/user_settings.html', 
            {'update_user_form': update_user_form, 'update_profile_form': update_profile_form})
    
    else:
        return redirect(reverse('lanex:show_user', 
                                kwargs={'user_profile_slug': user_profile_slug}))


@login_required
def user_delete(request, user_profile_slug):
    if user_profile_slug == request.user.username:
        User.objects.filter(username=user_profile_slug).delete()
        return redirect("lanex:index")
    else:
        return redirect(reverse('lanex:show_user', 
                                kwargs={'user_profile_slug': user_profile_slug}))



## Previus code, Dead code; leaving for a bit in case need to adapt some parts later
"""
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
"""
"""
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

"""

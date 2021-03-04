import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'langex.settings')

import django
django.setup()
from lanex.models import Language, LanguageRequest, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import random

def populate():

    # Creates Users to assign as Creators
    example_users = [
        {'username': 'username1',
        'password': 'french',
        'email': 'user1@ok.com'},
        {'username': 'username2',
        'password': 'spanish',
        'email': 'user2@ok.com'},
        {'username': 'username3',
        'password': 'japanese',
        'email': 'user3@ok.com'},
    ]



    french_requests = [
        {'title': 'Foo1',
        'desc': 'Foo',
        'views': 128},
        {'title': 'Foo2',
        'desc': 'Foo',
        'views': 64},
        {'title': 'Foo3',
        'desc': 'Foo',
        'views': 32},
    ]

    

    spanish_requests = [
        {'title': 'Foo1',
        'desc': 'Foo',
        'views': 64},
        {'title': 'Foo2',
        'desc': 'Foo',
        'views': 32},
        {'title': 'Foo3',
        'desc': 'Foo',
        'views': 16},
    ]

    japanese_requests = [
        {'title': 'Foo1',
        'desc': 'Foo',
        'views': 64},
        {'title': 'Foo2',
        'desc': 'Foo',
        'views': 32},
        {'title': 'Foo3',
        'desc': 'Foo',
        'views': 16},
    ]

    english_requests = [
        {'title': 'Foo1',
        'desc': 'Foo',
        'views': 64},
        {'title': 'Foo2',
        'desc': 'Foo',
        'views': 32},
        {'title': 'Foo3',
        'desc': 'Foo',
        'views': 16},
    ]

    other_requests = [
        {'title': 'Foo1',
        'desc': 'Foo',
        'views': 32},
        {'title': 'Foo2',
        'desc': 'Foo',
        'views': 16},
        {'title': 'Foo3',
        'desc': 'Foo',
        'views': 16},
    ]



    languages = {'French': {'requests': french_requests, 'picture': 'languages/french.jpg'},
            'Spanish': {'requests': spanish_requests, 'picture': 'languages/spanish.jpg'},
            'Japanese': {'requests': japanese_requests, 'picture': 'languages/japanese.jpg'},
            'English': {'requests': english_requests, 'picture': 'languages/english.jpg'},
            'Others': {'requests': other_requests, 'picture': 'languages/default.jpg'} }



    user_list = []
    for u in example_users:
        user_to_add = add_user(u['username'],u['password'],u['email'])
        user_list.append(user_to_add)
        print(f'- Added example user {user_to_add}')


    for language, language_data in languages.items():
        l = add_language(language, language_data['picture'])
        for r in language_data['requests']:
            add_request(l, r['title'], r['desc'], user_list[random.randint(0,2)], r['views'])


    for lang in Language.objects.all():
        for r in LanguageRequest.objects.filter(language=lang):
            print(f'- {lang}: {r}')



def get_random_name(situation):
    if situation == "first":
        first_names = ['Alexios','Minerva','Jun','Vladmir','Francesca','Ezio','Dumbledore','Zelda','Robin','Jeff','Lea','Pikachu']
        return random.choice(first_names)
    if situation == "last":
        last_names = ['Jeagar','Hisham','Chan','Freicks','Cocopops','D Luffy']
        return random.choice(last_names)


def add_request(language, title, desc, creator, views=0):
    r = LanguageRequest.objects.get_or_create(language=language, title=title, creator=creator, desc=desc, views=views)[0]
    return r


def add_language(name, picture):
    lang = Language.objects.get_or_create(name=name, picture=picture)[0]
    lang.save()
    return lang


def add_user(username, password, email):
    user_to_add = User(username=username, email=email, password=make_password(password), first_name=get_random_name("first"), last_name=get_random_name("last"))
    user_to_add.save()
    user_prof = UserProfile.objects.get_or_create(user=user_to_add)[0]
    user_prof.save()
    return user_to_add



if __name__ == '__main__':
    print('Yer a wizard, Harry...')
    populate()

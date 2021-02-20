import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'langex.settings')

import django
django.setup()
from lanex.models import Language, LanguageRequest

def populate():
    french_requests = [
        {'title': 'Je veux parler en français avec qqn',
        'url': 'https://moi.abc/',
        'views': 128},
        {'title': 'I speak Spanish, looking for a French speaker to talk with',
        'url': 'https://lui.def/',
        'views': 60},
    ]

    spanish_requests = [
        {'title': 'Interested in setting up a Spanish reading club!',
        'url': 'https://spa.abc/',
        'views': 64},
        {'title': 'Looking to polish up on my Spanish, anyone willing to help?',
        'url': 'https://yo.def/',
        'views': 32},
    ]

    japanese_requests = [
        {'title': '銀魂はすごいです',
        'url': 'https://ja.abc/',
        'views': 64},
        {'title': 'じゃない',
        'url': 'https://ek.def/',
        'views': 16},
    ]
    """ # Modifier d'autre temps
    other_requests = [
        {'title': 'language x',
        'url': 'https://ek.foo/',
        'views': 64},
    ]
    """

    languages = {'French': {'requests': french_requests, 'views': 128, 'likes': 64},
                'Spanish': {'requests': spanish_requests, 'views': 64, 'likes': 32},
                'Japanese': {'requests': japanese_requests, 'views': 32, 'likes': 16} }

    for language, language_data in languages.items():
        lang = add_language(language, language_data['views'], language_data['likes'])
        for r in language_data['requests']:
            add_request(lang, r['title'], r['url'], r['views'])
    
    for lang in Language.objects.all():
        for r in LanguageRequest.objects.filter(language=lang):
            print(f'- {lang}: {r}')


def add_request(language, title, url, views=0):
    r = LanguageRequest.objects.get_or_create(language=language, title=title)[0]
    r.url = url
    r.views = views
    r.save()
    return r


def add_language(name, views=0, likes=0):
    lang = Language.objects.get_or_create(name=name, views=views, likes=likes)[0]
    lang.save()
    return lang


if __name__ == '__main__':
    print('Starting Lanex population script...')
    populate()
from django.contrib.auth.context_processors import auth


def user(request):
    return {'user': auth(request)['user']}

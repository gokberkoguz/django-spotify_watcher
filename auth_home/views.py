from django.shortcuts import render


def home_page(request):
    if request.user.is_authenticated:
        print('USER ACCESS')
        print(request.user)
    else:
        print('USER CANT ACCESS')
        print(request.user)
    return render(request, 'home_landing.html')


def login_page(request):
    '''
    user = User.objects.get(id=1)
    social = user.social_auth.get(provider='spotify')
    token=social.extra_data['access_token']
    '''

    return render(request, 'login_page.html')
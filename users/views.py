from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import vk_requests


@login_required
def vk_friends_list(request):
    result = []
    api = vk_requests.create_api(service_token="15c6cc8115c6cc8115c6cc81ff15b72daf115c615c6cc814b7ddf741c8620f0819633cc")
    friends = api.friends.get(user_id=80692356, fields=['nickname', 'city'])
    print(friends)
    for i in friends['items']:
        result.extend([i['id'], i['first_name'], i['last_name']])
    context = {'result': result}
    return render(request, 'users/profile.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('apple:index'))


def register(request):
    if request.method != "POST":
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('apple:index'))

    context = {'form': form}
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    user = User.objects.get(username=request.user)

    context = {'user': user}
    return render(request, 'users/profile.html', context)

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('LearnLogs:index'))


def register(request):
    """Register a new user"""
    if request.method != 'POST':
        """Show an empty form"""
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # login automatically, region to the index home page
            authenticated_user = authenticate(
                username=new_user.username, password=request.POST['passwordl'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('LearnLogs:index'))

    context = {'form': form}
    return render(request, 'users/register.html', context)

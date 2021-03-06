from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from accounts.forms import SignUpForm, ChangeDefaultTimesForm
from .models import UserProfile
from django.contrib.auth.models import User


# Create your views here.
def create_account_view(request, *args, **kwargs):
    # Only process if a post request is sent
    if request.method == 'POST':

        create_account_form = SignUpForm(request.POST)

        # If the form has correct information it can be stored
        if create_account_form.is_valid():
            create_account_form.save()
            username = create_account_form.cleaned_data.get('username')
            password = create_account_form.cleaned_data.get('password1')
            email = create_account_form.cleaned_data.get('email')

            # Login to the account instantly
            user = authenticate(username=username, password=password)
            login(request, user)

            # Return back to the main screen
            return redirect('index')
    else:
        create_account_form = SignUpForm()

    my_context = {
        'form': create_account_form,
    }

    return render(request, 'accounts/create_account.html', my_context)


def profile_view(request):
    user = User.objects.get(username=request.user.username)
    context = {
        'user': user
    }
    return render(request, 'accounts/profile.html', context)


def change_default_times_view(request):
    user_profile = User.objects.get(username=request.user.username).userprofile
    form = ChangeDefaultTimesForm(request.POST or None, instance=user_profile)

    if form.is_valid():
        form.save()
        return redirect('profile')

    context = {
        'UserProfile': user_profile,
        'form': form
    }

    return render(request, 'accounts/change_default_times.html', context)

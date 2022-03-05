from django.contrib.auth import login, get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, UpdateView

from .forms import MyUserCreateForm, UserChangeForm, PasswordChangeForm


def register_view(request):
    form = MyUserCreateForm()
    if request.method == 'POST':
        form = MyUserCreateForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            url = request.GET.get('next')
            if url:
                return redirect(url)
            return redirect('webapp:index')
    return render(request, 'registration/registration.html', {'form' : form})

class ProfileDetailView(LoginRequiredMixin ,DetailView):
    model = get_user_model()
    template_name = 'profile.html'
    context_object_name = 'user_obj'

class UserChangeView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'user_change.html'
    form_class = UserChangeForm
    context_object_name = 'user_obj'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.object.pk})



class UserPasswordChangeView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'user_password_change.html'
    form_class = PasswordChangeForm
    context_object_name = 'user_obj'

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk' : self.object.pk})

    def get_object(self, queryset=None):
        return self.request.user
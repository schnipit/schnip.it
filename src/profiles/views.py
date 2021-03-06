from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.models import User
from account.views import SettingsView
from .forms import ProfileSettingsForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class ProfileSettingsView(SettingsView):
    form_class = ProfileSettingsForm
    
    def update_account(self, form):
        super(ProfileSettingsView, self).update_account(form)

        print (dir(form))
        
        profile = self.request.user.profile
        profile.bio = form.cleaned_data["bio"]
        profile.avatar = form.cleaned_data["avatar"]
        profile.sub1 = form.cleaned_data["sub1"]
        profile.sub2 = form.cleaned_data["sub2"]
        profile.save()

    def get_initial(self):
        initial = super(ProfileSettingsView, self).get_initial()
        initial["bio"] = self.request.user.profile.bio
        initial["avatar"] = self.request.user.profile.avatar
        return initial

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class ProfileDetailView(DetailView):
    model = User
    context_object_name = "profile_user"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if "pk" not in kwargs:
            self.kwargs["pk"] = request.user.pk
            kwargs["pk"] = request.user.pk

        return super().get(request, *args, **kwargs)

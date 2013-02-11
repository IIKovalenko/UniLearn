from django.views.generic import FormView, View, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from braces.views import LoginRequiredMixin

from .models import UserProfile, UserTestStatistics


class LoginView(FormView):
    template_name = 'account/login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
        if user:
            login(self.request, user)
            return self.success_redirect()

    def success_redirect(self):
        if self.request.GET.get('next'):
            return redirect(self.request.GET.get('next'))
        else:
            return redirect(reverse('index'))


class LogoutView(View):

    def post(self, request):
        logout(request)
        return redirect(request.GET.get('next') or reverse('index'))

    def get(self, request):
        return self.post(request)

class ProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = 'account/profile_detail.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['not_passed_statuses'] = UserTestStatistics.objects.filter(user=self.request.user,
                                                                         status=UserTestStatistics.TEST_STATUSES.not_passed)
        context['failed_statuses'] = UserTestStatistics.objects.filter(user=self.request.user,
                                                                         status=UserTestStatistics.TEST_STATUSES.failed)
        return context

from django.views.generic import FormView, View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


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


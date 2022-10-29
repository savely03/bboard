import time
from django.shortcuts import render
from django.template.loader import get_template
from django.http import Http404, HttpResponse
from django.template import TemplateDoesNotExist
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView
from .forms import AvdUserForm
from .models import AvdUser
from django.urls import reverse_lazy
from django.contrib import messages


def index(request):
    return render(request, 'main/index.html')


def other_page(request, page):
    try:
        template = get_template(f'main/{page}.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


class BBLoginView(LoginView):
    template_name = 'main/login.html'


class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


@login_required
def change_user_view(request):
    form = AvdUserForm(instance=request.user)
    if request.method == 'POST':
        form = AvdUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные пользователя успешно изменены')
    return render(request, 'main/change_user_info.html', context={'form': form})


@login_required
def profile(request):
    return render(request, 'main/profile.html')

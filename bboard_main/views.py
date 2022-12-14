from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.http import Http404, HttpResponse
from django.template import TemplateDoesNotExist
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import AvdUserForm, BbForm
from .models import AvdUser, SubRubric, Bb, Comment
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView
from .forms import RegisterUserForm, UserCommentForm, GuestCommentForm
from django.views.generic import DeleteView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.core.mail import send_mail


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


class BBLogoutConfirmView(TemplateView):
    template_name = 'main/logout_confirm.html'


class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


class RegisterUserView(CreateView):
    model = AvdUser
    form_class = RegisterUserForm
    template_name = 'main/register_user.html'
    success_url = reverse_lazy('register_done')


class BBDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = AvdUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('index')
    success_message = 'Ваш аккаунт успешно удален'


def register_done(request):
    return render(request, 'main/register_done.html')


def change_password(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменен!')
            return redirect('change_password')
        else:
            messages.error(request, 'Ошибка. Проверьте правильность введенного пароля.')
    return render(request, 'main/password_change.html', context={'form': form})


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
    bbs = Bb.objects.filter(author=request.user.pk, is_active=True)
    paginator = Paginator(bbs, 3)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page_obg = paginator.get_page(page_num)
    return render(request, 'main/profile.html', context={'bbs': page_obg.object_list, 'page': page_obg})


def profile_bb_detail(request):
    pass


@login_required
def profile_bb_add(request):
    form = BbForm()
    if request.method == 'POST':
        form = BbForm(request.POST, request.FILES)
        if form.is_valid():
            bb = form.save(commit=False)
            bb.author = request.user
            form.save()
            messages.success(request, 'Объявление успешно добавлено.')
    return render(request, 'main/profile_bb_add.html', context={'form': form})


@login_required
def profile_bb_delete(request, pk):
    bb = get_object_or_404(Bb, pk=pk)
    if request.method == 'POST':
        if bb:
            bb.delete()
            return redirect('delete_done')
    return render(request, 'main/profile_bb_delete.html', context={'bb': bb})


class ProfileDeleteDone(TemplateView):
    template_name = 'main/profile_bb_delete_done.html'


@login_required
def profile_bb_change(request, pk):
    bb = get_object_or_404(Bb, pk=pk)
    form = BbForm(instance=bb)
    if request.method == 'POST':
        form = BbForm(request.POST, instance=bb)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объявление успешно изменено.')
    return render(request, 'main/profile_bb_change.html', context={'form': form})


def by_rubric(request, pk):
    rubric = get_object_or_404(SubRubric, pk=pk)
    bbs = Bb.objects.filter(is_active=True, rubric=pk)
    paginator = Paginator(bbs, 3)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page_obj = paginator.get_page(page_num)
    context = {'rubric': rubric, 'page': page_obj, 'bbs': page_obj.object_list}
    return render(request, 'main/by_rubric.html', context=context)


def detail(request, pk):
    bb = get_object_or_404(Bb, pk=pk)
    initial = {'bb': bb.pk}
    comments = Comment.objects.filter(bb=bb, is_active=True)
    if request.user.is_authenticated:
        initial['author'] = request.user.username
        form_class = UserCommentForm
    else:
        form_class = GuestCommentForm
    form = form_class(initial=initial)
    if request.method == 'POST':
        c_form = form_class(request.POST)
        if c_form.is_valid():
            if request.user.is_authenticated:
                subject = 'Добавлен новый комментарий.'
                message = f'Уважаемый {request.user.username.title()}, ' \
                          f'вы добавили новый комментарий к объявлению ({bb.title}).'
                send_mail(subject, message, 'admin@yandex.ru', ['savely.domnikov@yandex.ru'])
            c_form.save()
            messages.success(request, 'Комментарий успешно добавлен.')
        else:
            form = c_form
            messages.error(request, 'Комментарий не добавлен')
    return render(request, 'main/detail.html', context={'bb': bb, 'form': form, 'comments': comments})

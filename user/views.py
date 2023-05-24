from django.apps import apps
from django.db.models import Case, When
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import *
from django.views.generic import UpdateView
from comp.models import History
from django.contrib.auth.models import User
from .forms import ChangePassForm, UserRegisterForm, UserLoginForm, UserUpdateForm
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import logout, login

# Create your views here.


class HistoryView(View):
    template_name = 'user/history.html'

    def get(self, request):
        if request.user.is_authenticated:
            val = []
            his = []
            field = []
            date = []
            us = User.objects.filter(id=request.user.id).get()
            d = History.objects.filter(user_id=us).values(
                'result', 'comp_type', 'date').order_by('-date')
            data = list(d)
            for item in data:
                lst = item['result'].split(' ')
                model_name = apps.get_model('comp', item['comp_type'])
                if item['comp_type'] == 'RAM':
                    val = ['name', 'capacity',
                           'frequency', 'memory_type__name']
                    fields = ['Name', 'Capacity', 'Frequency', 'Memory Type']
                elif item['comp_type'] == 'Processor':
                    val = ['name', 'cores', 'frequency', 'socket__name']
                    fields = ['Name', 'Cores', 'Frequency', 'Socket']
                elif item['comp_type'] == 'GrapCard':
                    val = ['name', 'video_memory',
                           'proc_frequency', 'effective_mem_freq']
                    fields = ['Name', 'Video Memory(GB)',
                              'Graphic Processor Frequency(GHz)', 'Effective Memory Frequency(GHz)']
                elif item['comp_type'] == 'Motherboard':
                    val = ['name', 'socket__name',
                           'memory_type__name', 'max_memory']
                    fields = ['Name', 'Socket',
                              'Memory Type', 'Max Memory(GB)']
                preserved = Case(*[When(pk=pk, then=pos)
                                   for pos, pk in enumerate(lst)])
                queryset = list(model_name.objects.filter(
                    pk__in=lst).order_by(preserved).values(*val))
                his.append(queryset)
                field.append(fields)
                date.append(item['date'])
            fin_list = zip(his, field, date)
            dict = {
                'data': fin_list,
                'fields': field
            }
        return render(request, self.template_name, dict)


class UpdateUser(UpdateView):
    form_class = UserUpdateForm
    template_name = 'user/update_user.html'
    success_url = reverse_lazy('edit_profile')

    def get_object(self):
        return self.request.user


class PassChangeView(PasswordChangeView):
    form_class = ChangePassForm
    success_url = reverse_lazy('edit_success')
    template_name = 'user/pass_change.html'


def PassEditSuccess(request):
    return render(request, 'user/edit_success.html')


class RegisterUser(CreateView):
    form_class = UserRegisterForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = UserLoginForm
    template_name = 'user/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


def LogoutUser(request):
    logout(request)
    return redirect('login')

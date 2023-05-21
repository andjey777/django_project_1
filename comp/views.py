import datetime
from django.apps import apps
from django.db.models import F, Case, When
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import *
from django.contrib.auth.models import User
from .forms import ChangePassForm, RAMForm, UserRegisterForm, UserLoginForm, UserUpdateForm
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import logout, login

# Create your views here.


def Recommend(request):
    dict = {}
    if request.method == 'POST':
        option = request.POST['drop']
        if option == 'RAM':
            query = RAM.objects.select_related('memory_type').values(
                'name', 'capacity', 'frequency', 'memory_type__name').order_by('recomend')[:10]
            fields = ['Name', 'Capacity(GB)', 'Frequency(GHz)', 'Memory Type']
        if option == 'Processor':
            query = Processor.objects.select_related('socket').values(
                'name', 'cores', 'frequency', 'socket__name').order_by('recomend')[:10]
            fields = ['Name', 'Cores', 'Frequency(GHz)', 'Socket']
        if option == 'GrapCard':
            query = GrapCard.objects.values(
                'name', 'video_memory', 'proc_frequency', 'effective_mem_freq').order_by('recomend')[:10]
            fields = ['Name', 'Video Memory(GB)',
                      'Graphic Processor Frequency(GHz)', 'Effective Memory Frequency(GHz)']
        if option == 'Motherboard':
            query = Motherboard.objects.select_related('memory_type', 'soket').values(
                'name', 'chipset', 'memory_type__name', 'socket__name', 'max_memory').order_by('recomend')[:10]
            fields = ['Name', 'Chipset', 'Memory Type', 'Socket', 'Max Memory(GHz)']
        lst = list(query)
        dict = {
            'model': lst,
            'fields': fields
        }
    return render(request, 'comp/recom.html', dict)


def GetGrCard(request):
    dict = {}
    if request.method == 'POST':
        cap = int(request.POST['vid_mem'])
        grFreq = int(request.POST['grFreq'])
        memFreq = int(request.POST['memFreq'])
        param = [cap, grFreq, memFreq]
        fields = ['Name', 'Video Memory(GB)',
                  'Graphic Processor Frequency(GHz)', 'Effective Memory Frequency(GHz)']
        res = Calculate(param, list(
            GrapCard.objects.values_list('id', 'video_memory', 'proc_frequency', 'effective_mem_freq')))
        preserved = Case(*[When(pk=pk, then=pos)
                         for pos, pk in enumerate(res)])
        queryset = list(GrapCard.objects.filter(pk__in=res).order_by(preserved).values(
            'name', 'video_memory', 'proc_frequency', 'effective_mem_freq'))
        if len(res) != 0:
            inc = GrapCard.objects.get(pk=res[0])
            inc.recomend = F('recomend') + 1
            inc.save()
        dict = {
            'res': queryset,
            'fields': fields
        }
        SaveToDB('GrapCard', res, request)
    return render(request, 'comp/grCard.html', dict)


def GetProc(request):
    dict = {}
    if request.method == 'POST':
        cap = int(request.POST['cores'])
        freq = int(request.POST['freq'])
        socket = request.POST['socket_sel']
        param = [cap, freq]
        fields = ['Name', 'Cores', 'Frequency(GHz)', 'Socket']
        if socket == 'none':
            res = Calculate(param, list(
                Processor.objects.values_list('id', 'cores', 'frequency')))
        else:
            res = Calculate(param, list(
                Processor.objects.filter(
            socket__name=socket).values_list('id', 'cores', 'frequency')))
        preserved = Case(*[When(pk=pk, then=pos)
                         for pos, pk in enumerate(res)])
        queryset = list(Processor.objects.filter(pk__in=res).order_by(preserved).select_related(
            'socket').values('name', 'cores', 'frequency', 'socket__name'))
        if len(res) != 0:
            inc = Processor.objects.get(pk=res[0])
            inc.recomend = F('recomend') + 1
            inc.save()
        dict = {
            'res': queryset,
            'fields': fields
        }
        SaveToDB('Processor', res, request)
    dict['socket'] = list(Socket.objects.values('name'))
    return render(request, 'comp/proc.html', dict)


def GetRam(request):
    dict = {}
    if request.method == 'POST' and request.user.is_authenticated:
        cap = int(request.POST['cap'])
        freq = int(request.POST['freq'])
        mem_type = request.POST['mem_sel']
        param = [cap, freq]
        fields = ['Name', 'Capacity(GB)', 'Frequency(GHz)', 'Memory Type']
        if mem_type == 'none':
            res = Calculate(param, list(
                RAM.objects.values_list('id', 'capacity', 'frequency')))
        else:
            res = Calculate(param, list(
                RAM.objects.filter(
            memory_type__name=mem_type).values_list('id', 'capacity', 'frequency')))
        preserved = Case(*[When(pk=pk, then=pos)
                         for pos, pk in enumerate(res)])
        queryset = list(RAM.objects.filter(pk__in=res).order_by(preserved).select_related(
            'memory_type').values('name', 'capacity', 'frequency', 'memory_type__name'))
        if len(res) != 0:
            inc = RAM.objects.get(pk=res[0])
            inc.recomend = F('recomend') + 1
            inc.save()
        dict = {
            'res': queryset,
            'fields': fields
        }
        SaveToDB('RAM', res, request)
    dict['mem_type'] = list(MemoryType.objects.values('name'))
    return render(request, 'comp/ram.html', dict)


def GetMotherboard(request):
    dict = {}
    if request.method == 'POST' and request.user.is_authenticated:
        socket = request.POST['socket_sel']
        mem_type = request.POST['mem_sel']
        max_mem = int(request.POST['max_memory'])
        param = [max_mem]
        fields = ['Name', 'Socket', 'Memory Type', 'Max Memory(GB)']
        res = Calculate(param, list(Motherboard.objects.filter(
            socket__name=socket, memory_type__name=mem_type).values_list('id', 'max_memory')))
        preserved = Case(*[When(pk=pk, then=pos)
                         for pos, pk in enumerate(res)])
        queryset = list(Motherboard.objects.filter(pk__in=res).order_by(preserved).select_related(
            'memory_type', 'socket').values('name', 'socket__name', 'memory_type__name', 'max_memory'))
        if len(res) != 0:
            inc = Motherboard.objects.get(pk=res[0])
            inc.recomend = F('recomend') + 1
            inc.save()
        dict = {
            'res': queryset,
            'fields': fields
        }
        SaveToDB('Motherboard', res, request)
    dict['socket'] = list(Socket.objects.values('name'))
    dict['mem_type'] = list(MemoryType.objects.values('name'))
    return render(request, 'comp/motherboard.html', dict)


def SaveToDB(model, ids, request):
    us = User.objects.filter(id=request.user.id).get()
    if History.objects.filter(user_id=us).count() == 10:
        earliest = History.objects.filter(user_id=us).earliest('date')
        earliest.result = ' '.join(str(x) for x in ids)
        earliest.date = datetime.datetime.now()
        earliest.comp_type = model
        earliest.save()
    else:
        h = History.objects.create(
            user_id=us, result=' '.join(str(x) for x in ids), comp_type=model, date=datetime.datetime.now())


def Calculate(param, lis):
    wei_list = []
    result = []
    for item in lis:
        t = 0
        for i in range(len(param)):
            t += abs(param[i] - item[i+1]) / param[i]
        # cr = abs(field1 - item[1]) / field1
        # f = abs(field2 - item[2]) / field2
        wei_list.append({'id': item[0], 'wei': t})
    # print(r)
    newlist = sorted(wei_list, key=lambda d: d['wei'])[:10]
    # print(newlist[:2])
    for item in newlist:
        result.append(item['id'])
    return result


def OutputInfo(request):
    dict = {}
    if request.method == 'POST':
        option = request.POST['drop']
        if option == 'RAM':
            query = RAM.objects.select_related('memory_type').values(
                'name', 'capacity', 'frequency', 'memory_type__name')
            fields = ['Name', 'Capacity(GB)', 'Frequency(GHz)', 'Memory Type']
        elif option == 'Processor':
            query = Processor.objects.select_related('socket').values(
                'name', 'cores', 'frequency', 'socket__name')
            fields = ['Name', 'Cores', 'Frequency(GHz)', 'Socket']
        elif option == 'GrapCard':
            query = GrapCard.objects.values(
                'name', 'video_memory', 'proc_frequency', 'effective_mem_freq')
            fields = ['Name', 'Video Memory(GB)',
                      'Graphic Processor Frequency(GHz)', 'Effective Memory Frequency(GHz)']
        elif option == 'Motherboard':
            query = Motherboard.objects.select_related('memory_type', 'soket').values(
                'name', 'chipset', 'memory_type__name', 'socket__name', 'max_memory')
            fields = ['Name', 'Cores', 'Memory Type', 'Socket', 'Max Memory(GB)']
        lst = list(query)
        dict = {
            'model': lst,
            'fields': fields
        }
    return render(request, 'comp/info.html', dict)


def HistoryView(request):
    if request.user.is_authenticated:
        val = []
        his = []
        field = []
        date = []
        us = User.objects.filter(id=request.user.id).get()
        d = History.objects.filter(user_id=us).values('result', 'comp_type', 'date').order_by('-date')
        data = list(d)
        for item in data:
            lst = item['result'].split(' ')
            model_name = apps.get_model('comp', item['comp_type'])
            if item['comp_type'] == 'RAM':
                val = ['name', 'capacity', 'frequency', 'memory_type__name']
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
    return render(request, 'comp/history.html', dict)


def BuilderView(request):
    dict = {}
    if request.method == 'POST' and request.user.is_authenticated:
        #Motherboard
        socket = request.POST['socket_sel']
        mem_type = request.POST['mem_sel']
        mb_param = [int(request.POST['max_memory'])]
        mb_fields = ['Name', 'Socket', 'Memory Type', 'Max Memory(GB)']
        mb_res = Calculate(mb_param, list(Motherboard.objects.filter(
            socket__name=socket, memory_type__name=mem_type).values_list('id', 'max_memory')))
        mb_preserved = Case(*[When(pk=pk, then=pos)
                         for pos, pk in enumerate(mb_res)])
        mb_queryset = list(Motherboard.objects.filter(pk__in=mb_res).order_by(mb_preserved).select_related(
            'memory_type', 'socket').values('name', 'socket__name', 'memory_type__name', 'max_memory'))
        #RAM
        ram_param = [int(request.POST['ram_cap']), int(request.POST['ram_freq'])]
        ram_fields = ['Name', 'Capacity(GB)', 'Frequency(GHz)', 'Memory Type']
        ram_res = Calculate(ram_param, list(
            RAM.objects.filter(memory_type__name=mem_type).values_list('id', 'capacity', 'frequency')))
        ram_preserved = Case(*[When(pk=pk, then=pos)
                         for pos, pk in enumerate(ram_res)])
        ram_queryset = list(RAM.objects.filter(pk__in=ram_res).order_by(ram_preserved).select_related(
            'memory_type').values('name', 'capacity', 'frequency', 'memory_type__name'))
        #Proc
        proc_param = [int(request.POST['proc_cores']), int(request.POST['proc_freq'])]
        proc_fields = ['Name', 'Cores', 'Frequency(GHz)', 'Socket']
        proc_res = Calculate(proc_param, list(
            Processor.objects.filter(socket__name=socket).values_list('id', 'cores', 'frequency')))
        proc_preserved = Case(*[When(pk=pk, then=pos)
                         for pos, pk in enumerate(proc_res)])
        proc_queryset = list(Processor.objects.filter(pk__in=proc_res).order_by(proc_preserved).select_related(
            'socket').values('name', 'cores', 'frequency', 'socket__name'))
        #Grap Card        
        gr_param = [int(request.POST['vid_mem']), int(request.POST['grFreq']), int(request.POST['memFreq'])]
        gr_fields = ['Name', 'Video Memory(GB)',
                  'Graphic Processor Frequency(GHz)', 'Effective Memory Frequency(GHz)']
        gr_res = Calculate(gr_param, list(
            GrapCard.objects.values_list('id', 'video_memory', 'proc_frequency', 'effective_mem_freq')))
        gr_preserved = Case(*[When(pk=pk, then=pos)
                         for pos, pk in enumerate(gr_res)])
        gr_queryset = list(GrapCard.objects.filter(pk__in=gr_res).order_by(gr_preserved).values(
            'name', 'video_memory', 'proc_frequency', 'effective_mem_freq'))
        dict = {
            'gr_fields': gr_fields,
            'proc_fields': proc_fields,
            'ram_fields': ram_fields,
            'mb_fields': mb_fields,
            'gr_res': gr_queryset,
            'proc_res': proc_queryset,
            'ram_res': ram_queryset,
            'mb_res': mb_queryset
        }
    dict['socket'] = list(Socket.objects.values('name'))
    dict['mem_type'] = list(MemoryType.objects.values('name'))
    return render(request, 'comp/builder.html', dict)


class UpdateUser(UpdateView):
    form_class = UserUpdateForm
    template_name = 'comp/update_user.html'
    success_url = reverse_lazy('edit_profile')

    def get_object(self):
        return self.request.user


class PassChangeView(PasswordChangeView):
    form_class = ChangePassForm
    success_url = reverse_lazy('edit_success')
    template_name = 'comp/pass_change.html'


def PassEditSuccess(request):
    return render(request, 'comp/edit_success.html')


class RegisterUser(CreateView):
    form_class = UserRegisterForm
    template_name = 'comp/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = UserLoginForm
    template_name = 'comp/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


def LogoutUser(request):
    logout(request)
    return redirect('login')


def MainView(request):
    return render(request, "comp/main.html")
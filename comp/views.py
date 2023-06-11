import datetime
from django.db.models import F, Case, When
from django.shortcuts import render
from django.views import *
from .models import History
from .models import *
from django.contrib.auth.models import User

# Create your views here.

ram_fields = ['Name', 'Capacity', 'Frequency', 'Memory Type']
proc_fields = ['Name', 'Cores', 'Frequency', 'Socket']
gr_fields = ['Name', 'Video Memory(GB)', 'Graphic Processor Frequency(GHz)',
             'Effective Memory Frequency(GHz)']
mb_fields = ['Name', 'Chipset', 'Socket', 'Memory Type', 'Max Memory(GB)']

class Recommend(View):
    template_name = 'comp/recom.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        option = request.POST['drop']
        if option == 'RAM':
            query = RAM.objects.select_related('memory_type').values(
                'name', 'capacity', 'frequency', 'memory_type__name').order_by('-recomend')[:10]
            fields = ram_fields
        if option == 'Processor':
            query = Processor.objects.select_related('socket').values(
                'name', 'cores', 'frequency', 'socket__name').order_by('-recomend')[:10]
            fields = proc_fields
        if option == 'GrapCard':
            query = GrapCard.objects.values(
                'name', 'video_memory', 'proc_frequency', 'effective_mem_freq').order_by('-recomend')[:10]
            fields = gr_fields
        if option == 'Motherboard':
            query = Motherboard.objects.select_related('memory_type', 'soket').values(
                'name', 'chipset', 'memory_type__name', 'socket__name', 'max_memory').order_by('-recomend')[:10]
            fields = mb_fields
        lst = list(query)
        dict = {
            'model': lst,
            'fields': fields
        }
        return render(request, self.template_name, dict)


class GetGrCard(View):
    template_name = 'comp/grCard.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if request.user.is_authenticated:
            cap = int(request.POST['vid_mem'])
            grFreq = int(request.POST['grFreq'])
            memFreq = int(request.POST['memFreq'])
            param = [cap, grFreq, memFreq]
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
                'fields': gr_fields
            }
            if len(queryset) > 0:
                SaveToDB('GrapCard', res, request)
        return render(request, self.template_name, dict)


class GetProc(View):
    template_name = 'comp/proc.html'
    dict = {}
    dict['socket'] = list(Socket.objects.values('name'))

    def get(self, request):
        return render(request, self.template_name, self.dict)

    def post(self, request):
        if request.user.is_authenticated:
            cap = int(request.POST['cores'])
            freq = int(request.POST['freq'])
            socket = request.POST['socket_sel']
            param = [cap, freq]
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
                'fields': proc_fields
            }
            if len(queryset) > 0:
                SaveToDB('Processor', res, request)
        return render(request, self.template_name, dict | self.dict)


class GetRam(View):
    template_name = 'comp/ram.html'
    dict = {}
    dict['mem_type'] = list(MemoryType.objects.values('name'))

    def get(self, request):
        return render(request, self.template_name, self.dict)

    def post(self, request):
        if request.user.is_authenticated:
            cap = int(request.POST['cap'])
            freq = int(request.POST['freq'])
            mem_type = request.POST['mem_sel']
            param = [cap, freq]
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
                'fields': ram_fields
            }
            if len(queryset) > 0:
                SaveToDB('RAM', res, request)
        return render(request, self.template_name, dict | self.dict)


class GetMotherboard(View):
    template_name = 'comp/motherboard.html'
    dict = {}
    dict['socket'] = list(Socket.objects.values('name'))
    dict['mem_type'] = list(MemoryType.objects.values('name'))

    def get(self, request):
        return render(request, self.template_name, self.dict)

    def post(self, request):
        if request.user.is_authenticated:
            socket = request.POST['socket_sel']
            mem_type = request.POST['mem_sel']
            max_mem = int(request.POST['max_memory'])
            param = [max_mem]
            res = Calculate(param, list(Motherboard.objects.filter(
                socket__name=socket, memory_type__name=mem_type).values_list('id', 'max_memory')))
            preserved = Case(*[When(pk=pk, then=pos)
                               for pos, pk in enumerate(res)])
            queryset = list(Motherboard.objects.filter(pk__in=res).order_by(preserved).select_related(
                'memory_type', 'socket').values('name', 'chipset', 'socket__name', 'memory_type__name', 'max_memory'))
            if len(res) != 0:
                inc = Motherboard.objects.get(pk=res[0])
                inc.recomend = F('recomend') + 1
                inc.save()
            dict = {
                'res': queryset,
                'fields': mb_fields
            }
            if len(queryset) > 0:
                SaveToDB('Motherboard', res, request)
        return render(request, self.template_name, dict | self.dict)


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


class OutputInfo(View):
    templtae_name = 'comp/info.html'

    def get(self, request):
        return render(request, self.templtae_name)

    def post(self, request):
        option = request.POST['drop']
        if option == 'RAM':
            query = RAM.objects.select_related('memory_type').values(
                'name', 'capacity', 'frequency', 'memory_type__name')
            fields = ram_fields
        elif option == 'Processor':
            query = Processor.objects.select_related('socket').values(
                'name', 'cores', 'frequency', 'socket__name')
            fields = proc_fields
        elif option == 'GrapCard':
            query = GrapCard.objects.values(
                'name', 'video_memory', 'proc_frequency', 'effective_mem_freq')
            fields = gr_fields
        elif option == 'Motherboard':
            query = Motherboard.objects.select_related('memory_type', 'soket').values(
                'name', 'chipset', 'memory_type__name', 'socket__name', 'max_memory')
            fields = mb_fields
        lst = list(query)
        dict = {
            'model': lst,
            'fields': fields
        }
        return render(request, self.templtae_name, dict)


class BuilderView(View):
    template_name = 'comp/builder.html'
    dict = {}
    dict['socket'] = list(Socket.objects.values('name'))
    dict['mem_type'] = list(MemoryType.objects.values('name'))

    def get(self, request):
        return render(request, self.template_name, self.dict)

    def post(self, request):
        if request.user.is_authenticated:
            # Motherboard
            socket = request.POST['socket_sel']
            mem_type = request.POST['mem_sel']
            mb_param = [int(request.POST['max_memory'])]
            mb_res = Calculate(mb_param, list(Motherboard.objects.filter(
                socket__name=socket, memory_type__name=mem_type).values_list('id', 'max_memory')))
            mb_preserved = Case(*[When(pk=pk, then=pos)
                                  for pos, pk in enumerate(mb_res)])
            mb_queryset = list(Motherboard.objects.filter(pk__in=mb_res).order_by(mb_preserved).select_related(
                'memory_type', 'socket').values('name', 'chipset', 'socket__name', 'memory_type__name', 'max_memory'))
            # RAM
            ram_param = [int(request.POST['ram_cap']),
                         int(request.POST['ram_freq'])]
            ram_res = Calculate(ram_param, list(
                RAM.objects.filter(memory_type__name=mem_type).values_list('id', 'capacity', 'frequency')))
            ram_preserved = Case(*[When(pk=pk, then=pos)
                                   for pos, pk in enumerate(ram_res)])
            ram_queryset = list(RAM.objects.filter(pk__in=ram_res).order_by(ram_preserved).select_related(
                'memory_type').values('name', 'capacity', 'frequency', 'memory_type__name'))
            # Proc
            proc_param = [int(request.POST['proc_cores']),
                          int(request.POST['proc_freq'])]
            proc_res = Calculate(proc_param, list(
                Processor.objects.filter(socket__name=socket).values_list('id', 'cores', 'frequency')))
            proc_preserved = Case(*[When(pk=pk, then=pos)
                                    for pos, pk in enumerate(proc_res)])
            proc_queryset = list(Processor.objects.filter(pk__in=proc_res).order_by(proc_preserved).select_related(
                'socket').values('name', 'cores', 'frequency', 'socket__name'))
            # Grap Card
            gr_param = [int(request.POST['vid_mem']), int(
                request.POST['grFreq']), int(request.POST['memFreq'])]
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
        return render(request, self.template_name, dict | self.dict)


def MainView(request):
    return render(request, "comp/main.html")

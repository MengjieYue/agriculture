# Create your views here.
#coding=utf-8
from django.core.exceptions import ObjectDoesNotExist
import StringIO
from django.shortcuts import render, redirect , render_to_response
import time,math, datetime,random
from random import uniform ,randint
from Captcha import display
from models import User,Storage,Sensor,Air,SoilMoist,SoilTemp,SunLight,COZ
import json
from django.http import HttpResponse
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from pylab import *
from django.utils.datastructures import SortedDict
import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import plot,savefig
import matplotlib.pyplot as plt
from django.db import transaction
from django.db import models
from django.core.validators import ValidationError
from django.contrib import admin


def index(request):
    #get
    if request.method == "GET":
        # get session
        function = request.session.get('function', '')
        warn_text = request.session.get('warn', '请输入用户名及密码')
        request.session.clear()
        return render(request, 'index.html', {
            "warn_text": warn_text, "function": function,
            'imgsrc': "/verifycode/?nocached=" + str(time.time()),
            # 'session_before': sess,
            # 'session_after': request.session.items()
        })

    #post
    elif request.method == "POST":
        code = request.POST['verifycode']
        session_code = request.session['django_captcha_key']
        if code.lower() == session_code.lower():
            #验证成功
            if "log" in request.POST:
                return login(request)
            if "reg" in request.POST:
                return register(request)
        else:
            #验证失败
            request.session['warn'] = '验证码错误，请重新输入'
            if "reg" in request.POST:
                request.session['function'] = 'regicurrent()'
            else:
                request.session['function'] = ''
            return redirect("/")


def verifycode(request):
    img_height = 20
    img_width = 70
    return display(request, img_height, img_width)


def login(request):
    uname = request.POST['username']
    try:
        user = User.objects.get(username=uname)
        if user.password == request.POST['password']:
            request.session.flush()
            request.session['has_loged'] = True
            user.statu=True
            user.save()
            return redirect('main', uname)
        else:
            request.session['function'] = ''
            request.session['warn'] = '密码错误，请重新输入'
            return redirect("/")
    except ObjectDoesNotExist:
        request.session['function'] = ''
        request.session['warn'] = '用户不存在，请重新输入'
        return redirect("/")


def register(request):
    uname = request.POST["username"]
    try:
        User.objects.get(username=uname)
        request.session['warn'] = '该用户已存在'
        request.session['function'] = 'regicurrent()'
        return redirect("/")
    except ObjectDoesNotExist:
        u = User()
        u.username = uname
        u.password = request.POST["password"]
        u.mail = request.POST['email']
        u.save()
        request.session['function'] = ''
        request.session['warn'] = '注册成功，请登录'
        return redirect("/")


def main(request, user):
    if request.session.get('has_loged', False):
        request.session['user'] = user
        return render(request, 'main.html', {
            "logeduser": user})
    else:
        return redirect("/")


def logout(request):
    uname = request.session.get('user', '')
    user = User.objects.get(username=uname)
    user.statu=False
    user.save()
    request.session.flush()
    return redirect("/")


def storagemanage(request):
    if request.method == "POST":
        return add(request)
    # if request.method == "GET":
    #     return alter(request)

    else:
        warn_text = request.session.get('warn1', '')
        if request.session.get('has_loged', False):
            user = request.session.get('user', '')
            storage_list=Storage.objects.filter(owner=user).order_by("index")

            return render(request, 'storagemanage.html', {
                "logeduser" : request.session['user'],
                "list":storage_list,
                "warn_text":warn_text})
        else:
            return redirect("/")


def storagemonitor(request):

    if request.session.get('has_loged', False):
        user = request.session.get('user', '')
        storage_list = Storage.objects.filter(owner__username__exact = user).order_by("index")
        sensor_list = Sensor.objects.filter(storage = storage_list[0]).filter(type='air').order_by("sensor_index")
        l=[]
        if storage_list[0].num_air !=0:
            l.append('空气温湿度')
        if storage_list[0].num_soilm !=0:
            l.append('土壤湿度')
        if storage_list[0].num_soilt !=0:
            l.append('土壤温度')
        if storage_list[0].num_sunlight !=0:
            l.append('光照')
        if storage_list[0].num_coz !=0:
            l.append('二氧化碳')

        return render(request, 'storagemonitor.html',{
            "logeduser":user,
            'sotrage_list':storage_list,
            "first_sensor":sensor_list,
            "first_type": l,
            })
    else:
        return redirect("/")


def delete(request, index):
    sensor_index=index
    s=Storage.objects.get(index=sensor_index)
    s.delete()
    return redirect('storagemanage')


def removeEmptyItem(list):
    for item in list:
        if item == '':
            list.remove(item)


def addSensor(len, index, addr, type, storage):
    for i in range(len):
        a=Sensor()
        a.sensor_index=index[i]
        a.storage=storage
        a.type=type
        a.location=addr[i]
        a.save()
        # name=''.join(str(storage), '_', str(index) )
        # fields={'time','data'}
        # create_model(name=name,fields=fields,app_label='sensorcontrol')


# @transaction.commit_on_success
# def alter(request):
#
#     index=request.GET['index']
#     air=request.GET.getlist('num_air[]')
#     soilt=request.GET.getlist('num_soilt[]')
#     soilm=request.GET.getlist('num_soilm[]')
#     light=request.GET.getlist('num_light[]')
#     coz=request.GET.getlist('num_coz[]')
#     addr_air=request.GET.getlist('Addr_air[]')
#     addr_soilt=request.GET.getlist('Addr_soilt[]')
#     addr_soilm=request.GET.getlist('Addr_soilm[]')
#     addr_light=request.GET.getlist('Addr_light[]')
#     addr_coz=request.GET.getlist('Addr_coz[]')
#     removeEmptyItem(air)
#     removeEmptyItem(soilt)
#     removeEmptyItem(soilm)
#     removeEmptyItem(light)
#     removeEmptyItem(coz)
#     removeEmptyItem(addr_air)
#     removeEmptyItem(addr_soilt)
#     removeEmptyItem(addr_soilm)
#     removeEmptyItem(addr_light)
#     removeEmptyItem(addr_coz)
#
#
#     s=Storage.objects.get(index=index)
#     u=request.session.get('user', '')
#     u1=User.objects.get(username=u)
#     s.owner=u1
#
#     s.num_air = len(air)
#     s.num_soilt = len(soilt)
#     s.num_soilm = len(soilm)
#     s.num_sunlight = len(light)
#     s.num_coz = len(coz)
#     s.nodeNum = s.num_air + s.num_coz + s.num_soilt + s.num_soilm + s.num_sunlight
#     s.index = index
#     s.save()
#     addSensor(s.num_air, air, addr_air, 'air', s)
#     addSensor(s.num_soilm, soilm, addr_soilm, 'soilm', s)
#     addSensor(s.num_soilt, soilt, addr_soilt, 'soilt', s)
#     addSensor(s.num_sunlight, light, addr_light, 'sun', s)
#     addSensor(s.num_coz, coz, addr_coz, 'coz', s)
#
#     return redirect('storagemanage')



@transaction.commit_on_success
def add(request):
    #request.encoding = 'gb2312'
    index=request.POST['index']
    air=request.POST.getlist('num_air[]')
    soilt=request.POST.getlist('num_soilt[]')
    soilm=request.POST.getlist('num_soilm[]')
    light=request.POST.getlist('num_light[]')
    coz=request.POST.getlist('num_coz[]')
    addr_air=request.POST.getlist('Addr_air[]')
    addr_soilt=request.POST.getlist('Addr_soilt[]')
    addr_soilm=request.POST.getlist('Addr_soilm[]')
    addr_light=request.POST.getlist('Addr_light[]')
    addr_coz=request.POST.getlist('Addr_coz[]')
    removeEmptyItem(air)
    removeEmptyItem(soilt)
    removeEmptyItem(soilm)
    removeEmptyItem(light)
    removeEmptyItem(coz)
    removeEmptyItem(addr_air)
    removeEmptyItem(addr_soilt)
    removeEmptyItem(addr_soilm)
    removeEmptyItem(addr_light)
    removeEmptyItem(addr_coz)

    try:
        Storage.objects.get(index=index)
        request.session['warn1'] = '该库房已存在'
        return redirect("/storagemanage/")
    except ObjectDoesNotExist:
        s=Storage()
        u=request.session.get('user', '')
        u1=User.objects.get(username=u)
        s.owner=u1

        s.num_air = len(air)
        s.num_soilt = len(soilt)
        s.num_soilm = len(soilm)
        s.num_sunlight = len(light)
        s.num_coz = len(coz)
        s.nodeNum = s.num_air + s.num_coz + s.num_soilt + s.num_soilm + s.num_sunlight
        s.index = index
        s.save()
        addSensor(s.num_air, air, addr_air, 'air', s)
        addSensor(s.num_soilm, soilm, addr_soilm, 'soilm', s)
        addSensor(s.num_soilt, soilt, addr_soilt, 'soilt', s)
        addSensor(s.num_sunlight, light, addr_light, 'sun', s)
        addSensor(s.num_coz, coz, addr_coz, 'coz', s)

        return redirect('storagemanage')


def gettemp(s_list,start,end,t):
    for i in s_list:
        a=Air.objects.filter(sensor_index=i).filter(time__range=(start, end))
        l=location(i.location)
        for b in a:
            t[l]=b.temp
    return t


def location(l):
    t = u'左下'
    if l == t:
        return(0)
    if l == u'中下':
        return(1)
    if l == u'右下':
        return(2)
    if l == u'左中':
        return(3)
    if l == u'中间':
        return(4)
    if l == u'右中':
        return(5)
    if l == u'左上':
        return(6)
    if l == u'中上':
        return(7)
    if l == u'右上':
        return(8)

    return(0)


def circlegraph(request,storage,type,year,month,day,hour,min):
    s_list=Sensor.objects.filter(storage__index__exact = storage).filter(type=type)
    year=int(year)
    month=int(month)
    day=int(day)
    hour=int(hour)
    min=int(min)

    n=[]


    t=np.zeros(9)
    p1=(2014,12,15,00,00,00,00,00,00)
    p2=(2014,12,15,00,00,00,00,00,00)
    start=datetime.datetime(year,month,day,hour,min,p1[5])
    end=datetime.datetime(year,month,day,hour,min,59)
    p=[]
    if type == 'air':
        t=gettemp(s_list,start,end,t)                     #下面的用不了函数，换数传递不了model变量

    if type == 'soilm':
        for i in s_list:
            a=SoilMoist.objects.filter(sensor_index=i).filter(time__range=(start, start))
            l=location(i.location)
            for b in a:
                t[l]=b.temp

    if type == 'soilt':
        for i in s_list:
            a=SoilTemp.objects.filter(sensor_index=i).filter(time__range=(start, start))
            l=location(i.location)
            for b in a:
                t[l]=b.temp

    if type == 'sun':
        for i in s_list:
            a=SunLight.objects.filter(sensor_index=i).filter(time__range=(start, start))
            l=location(i.location)
            for b in a:
                t[l]=b.light

    if type == 'coz':
        for i in s_list:
            a=COZ.objects.filter(sensor_index=i).filter(time__range=(start, end))
            l=location(i.location)
            for b in a:
                t[l]=b.content


    colors=[]
    legends = []
    for i in range(len(t)):
        if t[i]==0:
            colors.append('1')
            legends.append('null')
        else:
            #colors.append('r')
            colors.append(str((t[i]-4)/25))
            legends.append(str(t[i]))
    fig =Figure()
    a = np.arange(9,dtype=float).reshape(3,3)%3
    x = a.flatten()
    y = [0,0,0,1,1,1,2,2,2]
    m=np.zeros(9)
    n=np.zeros(9)
    for i in range(9):
        m[i]=x[i]+uniform(-0.2,0.2)
    for i in range(9):
        n[i]=y[i]+uniform(-0.2,0.2)
    tem = '*C'
    ax = fig.add_subplot(111)
    for i in range(len(x)):
        ax.scatter(m[i],n[i],color=colors[i],s=randint(500,8000))
        # ax.scatter([3],[0.1+i*0.2],color=colors[i],s=200)
        # ax.text(3.25,0.07+i*0.2,'%s %s' % (legends[i], tem))
        ax.annotate(legends[i],xy=(m[i],n[i]),xytext=(m[i]+0.2,n[i]+0.2))
    #ax.xlim((-0.5,4.5))
    #ax.ylim((-0.5,3))
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response


def linegraph(request,storage,sensor,year1,month1,day1,hour1,min1,year2,month2,day2,hour2,min2):
    s1=Sensor.objects.filter(storage=storage).filter(sensor_index=sensor)
    p1=(int(year1),int(month1),int(day1),int(hour1),int(min1),00,00,00,00)
    p2=(int(year2),int(month2),int(day2),int(hour2),int(min2),00,00,00,00)
    start_date2=time.mktime(p1)
    end_date2=time.mktime(p2)
    start_date=datetime.datetime(p1[0],p1[1],p1[2],p1[3],p1[4],p1[5])
    end_date=datetime.datetime(p2[0],p2[1],p2[2],p2[3],p2[4],p2[5])
    y1=[]
    y2=[]
    duration=0

    for s in s1:
        t=s.type

    # nlist=[]
    # data_list=Air.objects.filter(sensor_index=s).filter(time__range=(start_date,end_date))
    # for node in data_list:
    #      nlist.append({"index":node.id, "status":node.temp,"type":t})
    # sjson=json.dumps(nlist)
    # response=HttpResponse()
    # response['Content-type']="text/javascript"
    # response.write(sjson)
    # return response


        if t=='air':
            data_list=Air.objects.filter(sensor_index=s).filter(time__range=(start_date,end_date))
            duration=data_list.all().count()
            for d in data_list:
                #nlist.append(d.temp)
                y1.append(d.temp)
                y2.append(d.hum)

        if t=='soilt':
            data_list=SoilTemp.objects.filter(sensor_index=s).filter(time__range=(start_date,end_date))
            duration=data_list.all().count()
            for d in data_list:
                y1.append(d.temp)

        if t=='soilm':
            data_list=SoilMoist.objects.filter(sensor_index=s).filter(time__range=(start_date,end_date))
            duration=data_list.all().count()
            for d in data_list:
                y1.append(d.temp)

        if t=='sun':
            data_list=SunLight.objects.filter(sensor_index=s).filter(time__range=(start_date,end_date))
            duration=data_list.all().count()
            for d in data_list:
                y1.append(d.light)

        if t=='coz':
            data_list=COZ.objects.filter(sensor_index=s).filter(time__range=(start_date,end_date))
            duration=data_list.all().count()
            for d in data_list:
                y1.append(d.content)

    fig=Figure()
    ax =fig.add_subplot(111)
    hours=HourLocator()
    allminutes=MinuteLocator()
    hours_formatter=DateFormatter("%H"":""%M")
    timestamps=np.linspace(start_date2,end_date2,duration)
    dates=[datetime.datetime.fromtimestamp(ts) for ts in timestamps]

    #ax.xaxis.set_major_locator(hours)
    #ax.xaxis.set_minor_locator(allminutes)
    ax.xaxis.set_major_formatter(hours_formatter)
    ax.plot_date(dates,y1, 'm-',  marker='.',  linewidth=1)
    #fig.autofmt_xdate()

    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response


def getsensorlist(request,storage,type):
    sensor_list=Sensor.objects.filter(storage__index__exact=storage).filter(type=type).order_by('sensor_index')
    rlist = []
    for i in sensor_list:
        rlist.append(i.sensor_index)
    rjson = json.dumps(rlist)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(rjson)
    return response


def getsensorlist2(request,storage):
    sensor_list=Sensor.objects.filter(storage__index__exact=storage).order_by('sensor_index')
    rlist = []
    for i in sensor_list:
        rlist.append({"index":i.sensor_index, "type":i.type, "location":i.location})
    rjson = json.dumps(rlist)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(rjson)
    return response


def gettype(request,storage):
    s=Storage.objects.get(index=storage)
    l=[]
    if s.num_air !=0:
        l.append('air')
    if s.num_soilm !=0:
        l.append('soilm')
    if s.num_soilt !=0:
        l.append('soilt')
    if s.num_sunlight !=0:
        l.append('sun')
    if s.num_coz !=0:
        l.append('coz')

    rjson = json.dumps(l)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(rjson)
    return response



def create_model(name, fields=None, app_label='', module='', options=None, admin_opts=None):
    """
    创建指定model
    """
    class Meta:
        # Using type('Meta', ...) gives a dictproxy error during model creation
        pass

    if app_label:
        # app_label必须用Meta内部类来设定
        setattr(Meta, 'app_label', app_label)

    # 若提供了options参数，就要用更新Meta类
    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)

    # 创建一个字典来模拟类的声明，module和当前所在的module对应
    attrs = {'__module__': module, 'Meta': Meta}

    # 加入所有提供的字段
    if fields:
        attrs.update(fields)

    # 创建这个类，这会触发ModelBase来处理
    model = type(name, (models.Model,), attrs)

    # 如果提供了admin参数，那么创建Admin类
    if admin_opts is not None:
        class Admin(admin.ModelAdmin):
            pass
        for key, value in admin_opts:
            setattr(Admin, key, value)
        admin.site.register(model, Admin)

    return model


def install(model):
    from django.core.management import sql, color
    from django.db import connection

    style = color.no_style()

    cursor = connection.cursor()
    statements, pending = sql.sql_model_create(model, style)
    for sql in statements:
        cursor.execute(sql)

# def create_db_table(model_class):
#     """ Takes a Django model class and create a database table, if necessary.
#     """
#     # XXX Create related tables for ManyToMany etc
#     db.start_transaction()
#     table_name = model_class._meta.db_table
#
#     # Introspect the database to see if it doesn't already exist
#     if (connection.introspection.table_name_converter(table_name)
#                         not in connection.introspection.table_names()):
#
#         fields = _get_fields(model_class)
#
#         db.create_table(table_name, fields)
#         # Some fields are added differently, after table creation
#         # eg GeoDjango fields
#         db.execute_deferred_sql()
#         logger.debug("Created table '%s'" % table_name)
#
#     db.commit_transaction()
#
# def delete_db_table(model_class):
#     table_name = model_class._meta.db_table
#     db.start_transaction()
#     db.delete_table(table_name)
#     logger.debug("Deleted table '%s'" % table_name)
#     db.commit_transaction()
#



















# def write(request, type, num, sensor, storage):
#     n=num
#     s=Sensor.objects.filter(index=sensor).filter(storage__index__exact=storage)
#     storage=Storage.objects.get(index=storage)
#     for s1 in s:
#         if type == 'air':
#             for i in range(num):
#                 a=Air()
#                 a.sensor_index = s1
#                 a.storage=storage
#                 a.temp=uniform(15,25)
#                 a.hum=uniform(15,25)
#                 a.time=datetime.datetime(2014, 12, 22, randint(0, 24), randint(0, 60), 0)
#                 a.save()
#     return redirect('storagemanage')


# def data(request, id):
#     sensor=Sensor.objects.get(id=id)
#     rlist = []
#     rlist.append({"id" : id, "addr" : sensor.addr, "type" : sensor.type, "storage": sensor.storage})
#     rjson = json.dumps(rlist)
#     response = HttpResponse()
#     response['Content-Type'] = "text/javascript"
#     response.write(rjson)
#     return response


# def ShowNode(request,Station):
#     nodes_list = NodeInfo.objects.filter(station__station__exact = Station)
#     nlist=[]
#     for node in nodes_list:
#         nlist.append({"index":node.index, "status":node.status})
#     sjson=json.dumps(nlist)
#     response=HttpResponse()
#     response['Content-type']="text/javascript"
#     response.write(sjson)
#     return response



# def test(request):
#     nodes_list = NodeInfo.objects.filter(station__id__exact = 1)
#     num=nodes_list.all().count()
#     y=np.arange(num)
#     for i in range(len(y)):
#         y[i]=nodes_list[i].index
#
#     # def func(i):
#     #       return a[i]
#
#     #x=np.linspace(1,num,10)
#     x=np.arange(num)
#     plot(x,y,'--*b')
#     savefig('/home/nero/myfig.svg')
#
#     return redirect("/")
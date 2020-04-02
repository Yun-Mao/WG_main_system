import random
from . import models, forms
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from django.db.models import F
from django.db.models import Q

import json
from datetime import datetime
import xlwt
import xlrd
# Create your views here.
@login_required(login_url='/wgsite/login')
def index(request):
    page1 = 'active'
    if request.user.is_authenticated:
        username = request.user.username
        if request.user.is_superuser:
            super_admin = True
    messages.get_messages(request)
    return render(request, 'index.html', locals())


def login(request):
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            login_name = login_form.cleaned_data['username']
            login_password = login_form.cleaned_data['password']
            if User.objects.filter(username=login_name):
                user = authenticate(username=login_name,
                                    password=login_password)
                if user:
                    if user.is_active:
                        auth.login(request, user)
                        # messages.add_message(request, messages.SUCCESS, '登入成功')
                        return redirect('/wgsite')
                    else:
                        messages.add_message(request, messages.WARNING,
                                             '账号未启用')
                else:
                    messages.add_message(request, messages.WARNING, '密码错误')
            else:
                messages.add_message(request, messages.WARNING, '用户名不存在')
        else:
            messages.add_message(request, messages.INFO, '请检查输入的字段内容')
    else:
        login_form = forms.LoginForm()

    return render(request, 'login.html', locals())


def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, '成功注销')
    return redirect('/wgsite')


def register(request):
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            repassword = register_form.cleaned_data['repassword']
            if password == repassword:
                if User.objects.filter(username=username):
                    messages.add_message(request, messages.WARNING, '用户已存在')
                else:

                    user = User.objects.create_user(username=username,
                                                    password=password,
                                                    email=email)
                    user.save()
                    messages.add_message(request, messages.SUCCESS, '注册成功，请登录')
            else:
                messages.add_message(request, messages.WARNING, '两次密码不一致')
    else:
        register_form = forms.RegisterForm()
    return render(request, 'register.html', locals())


# 找回密码
def findPassword(request):
    button = '获取验证码'
    new_password = False
    if request.method == 'POST':
        username = request.POST.get('username', '')
        VerificationCode = request.POST.get('VerificationCode', '')
        password = request.POST.get('password', '')
        user = User.objects.filter(username=username)
        # 用户不存在
        if not user:
            tips = '用户' + username + '不存在'
            messages.add_message(request, messages.WARNING, tips)
        else:
            # 判断验证码是否已发送
            if not request.session.get('VerificationCode', ''):
                # 发送验证码并将验证码写入session
                button = '重置密码'
                tips = '验证码已发送'
                messages.add_message(request, messages.SUCCESS, tips)
                new_password = True
                VerificationCode = str(random.randint(1000, 9999))
                request.session['VerificationCode'] = VerificationCode
                user[0].email_user('找回密码', VerificationCode)
            # 匹配输入的验证码是否正确
            elif VerificationCode == request.session.get('VerificationCode'):
                # 密码加密处理并保存到数据库
                dj_ps = make_password(password, None, 'pbkdf2_sha256')
                user[0].password = dj_ps
                user[0].save()
                del request.session['VerificationCode']
                tips = '密码已重置'
                messages.add_message(request, messages.SUCCESS, tips)
            # 输入验证码错误
            else:
                tips = '验证码错误，请重新获取'
                messages.add_message(request, messages.WARNING, tips)
                new_password = False
                del request.session['VerificationCode']
    return render(request, 'forgot-password.html', locals())


@login_required(login_url='/wgsite/login')
def wsxx(request):
    page2 = 'active'
    page2_1 = 'active'
    page2_s = 'show'
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        user_id = request.user.id
        if request.user.is_superuser:
            super_admin = True
        if request.method == 'GET':
            changeWSXX = False
            information3 = forms.AddWsxxForm()  # 添加信息的框
            instance = models.MyUser.objects.filter(user_id=user_id)
            if instance:
                isWSXX = True  # 是否有完善信息的数据
                information = forms.WsxxModelForm(instance=instance[0])
                information2 = forms.ChangeWsxxModelForm(instance=instance[0])
                # information3 = forms.AddWsxxForm(instance[0])
            else:
                isWSXX = False
                information = forms.WsxxModelForm()
                information2 = forms.ChangeWsxxModelForm()
                # information3 = forms.AddWsxxForm()
            return render(request, 'wsxx.html', locals())
        else:
            temp = request.POST.get('changeWSXX', '')

            if temp != 'yes':
                instance = models.MyUser.objects.filter(user_id=user_id)
                if instance:  # 修改信息
                    information_change = forms.ChangeWsxxModelForm(
                        instance=instance[0], data=request.POST)
                    if information_change.is_valid():
                        realname = information_change.cleaned_data['realname']
                        sex = information_change.cleaned_data['sex']
                        phone_number = information_change.cleaned_data[
                            'phone_number']
                        college = information_change.cleaned_data['college']
                        information_change.save()
                        messages.add_message(request, messages.WARNING,
                                             "修改个人信息成功")
                        return redirect('/wgsite/wsxx')
                else:  # 增加信息
                    user = User.objects.get(id=user_id)
                    information_add = forms.AddWsxxForm(request.POST)
                    if information_add.is_valid():
                        realname = information_add.cleaned_data['realname']
                        sex = information_add.cleaned_data['sex']
                        phone_number = information_add.cleaned_data[
                            'phone_number']
                        college = information_add.cleaned_data['college']
                        myuser = models.MyUser.objects.create(
                            realname=realname,
                            sex=sex,
                            phone_number=phone_number,
                            college=college,
                            user=user)
                        myuser.save()
                        messages.add_message(request, messages.WARNING,
                                             "添加个人信息成功")
                        return redirect('/wgsite/wsxx')
            else:
                changeWSXX = True
                instance = models.MyUser.objects.filter(user_id=user_id)
                if instance:
                    isWSXX = True  # 是否有完善信息的数据
                    information = forms.WsxxModelForm(instance=instance[0])
                    information2 = forms.ChangeWsxxModelForm(
                        instance=instance[0])
                    # information3 = forms.AddWsxxForm(instance[0])
                else:
                    isWSXX = False
                    information = forms.WsxxModelForm()
                    information2 = forms.ChangeWsxxModelForm()
                    # information3 = forms.AddWsxxForm()
                return render(request, 'wsxx.html', locals())

    return render(request, 'wsxx.html', locals())


@login_required(login_url='/wgsite/login')
def mp(request):
    page_manage_people = 'active'
    if request.user.is_authenticated:
        username = request.user.username  # 获取用户名
        if request.user.is_superuser:  # 是否是高级账号
            super_admin = True

        # 管理员部分

        user_set2 = models.AdminUser.objects.select_related(
            'staffuser').values('staffuser__id')
        user_set = models.StaffUser.objects.values(
            'id', 'myuser__realname').exclude(id__in=user_set2)
        # user_set = list(user_set.difference(user_set2))

        # 工作人员部分

        staffuser_set2 = models.StaffUser.objects.select_related(
            'myuser').values('myuser__id')
        staffuser_set = models.MyUser.objects.values(
            'id', 'realname').exclude(id__in=staffuser_set2)

        if request.method == 'GET':
            information_add = forms.AdminUserForm(user_set)  # 添加管理员的框
            staffuser_add = forms.StaffUserForm(staffuser_set)  # 添加工作人员的框
            information_now = models.AdminUser.objects.values(
                'staffuser__id', 'staffuser__myuser__realname')
            staffuser_now = models.StaffUser.objects.values(
                'id', 'department', 'myuser__realname').order_by('department')
            return render(request, 'manage_people.html', locals())
        else:
            staff_user_id = request.POST.get('user', '')
            myuser_id = request.POST.get('staff_user', '')
            if staff_user_id != '':
                staff_user = models.StaffUser.objects.get(id=staff_user_id)
                # other = request.POST.get('other', '')
                information_add = forms.AddAdminUserForm(request.POST)
                if information_add.is_valid():
                    other = information_add.cleaned_data['other']
                    adminuser = models.AdminUser.objects.create(
                        other=other, staffuser=staff_user)
                    adminuser.save()
                    messages.add_message(request, messages.WARNING, "设为管理员成功")
                    return redirect('/wgsite/mp')
                else:
                    print('???')
            elif myuser_id != '':
                my_user = models.MyUser.objects.get(id=myuser_id)
                request_copy = request.POST.copy()
                request_copy['birthdate'] = datetime.strptime(
                    request_copy['birthdate'], '%m/%d/%Y')
                staffuser_add = forms.StaffUserForm(None, request_copy)
                if staffuser_add.is_valid():
                    department = staffuser_add.cleaned_data['department']
                    birthdate = staffuser_add.cleaned_data['birthdate']
                    other = staffuser_add.cleaned_data['staff_other']
                    staffuser = models.StaffUser.objects.create(
                        department=department,
                        birthdate=birthdate,
                        other=other,
                        myuser=my_user)
                    staffuser.save()
                    messages.add_message(request, messages.WARNING, "设为工作人员成功")
                    return redirect('/wgsite/mp')
                else:
                    print('???')
                    return render(request, 'manage_people.html', locals())
    return render(request, 'manage_people.html', locals())


@login_required(login_url='/wgsite/login')
def del_adim(request):
    itemid = request.GET.get('id')
    if request.method == 'POST':
        admin = get_object_or_404(Item, pk=itemid)
        admin.delete()


@login_required(login_url='/login/')
def bsproject(request):
    username = request.user.username
    if request.method == 'POST':
        print(1)
        if 'addbsproject' in request.POST:
            form = forms.BsProForm(request.POST)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, u"一个新的项目被添加.")
                    return redirect('/wgsite/bsproject')
                except Exception as e:
                    event = '新项目保存有一个问题: %s' % e
                    messages.warning(request, event)
            else:
                messages.warning(request, u'项目添加失败')
                return redirect('/wgsite/bsproject')

        # elif 'mark_done' in request.POST:
        #     del_list = request.POST.getlist('mark_done')

        #     models.BsProject.objects.filter(
        #         id__in=del_list).update(is_delete=True)
        #     messages.info(request, u'任务已经删除')

    else:
        form = forms.BsProForm()
    bsproject = models.BsProject.objects.all()
    return render(request, 'bsproject.html', locals())


@login_required(login_url='/login/')
def ebsproject(request, id):
    GetTask = get_object_or_404(models.BsProject, pk=id)
    if request.method == 'POST':
        form = forms.BsProForm(request.POST, instance=GetTask)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, u"项目修改完成.")
                return redirect('/wgsite/bsproject')
            except Exception as e:
                event = '新项目保存有一个问题: %s' % e
                messages.warning(request, event)
    else:
        form = forms.BsProForm(instance=GetTask)
        return render(request, 'baseform.html', locals())


@login_required(login_url='/login/')
def bmbsproject(request):
    username = request.user.username
    itemid = request.GET.get('id', '')
    if request.method == 'POST':

        myuser = models.MyUser.objects.filter(user_id=request.user.id)
        if myuser:
            bsproject = models.BsProject.objects.get(
                id=itemid)
            try:
                bm = models.BmBsProject.objects.create(
                    myuser=myuser[0], bsproject=bsproject)
                bm.save()
                event = '已报名'
                messages.warning(request, event)
            except Exception as e:
                event = '报名失败，请务重复报名，如果没有报上名请联系管理员'
                messages.warning(request, event)
        else:
            messages.add_message(request, messages.WARNING,
                                 "请先完善个人信息")
            return render(request, 'wsxx.html', locals())
        # if 'addbsproject' in request.POST:
        #     form = forms.BsProForm(request.POST)
        #     if form.is_valid():
        #         try:
        #             form.save()
        #             messages.success(request, u"一个新的项目被添加.")
        #             return redirect('/wgsite/bsproject')
        #         except Exception as e:
        #             event = '新项目保存有一个问题: %s' % e
        #             messages.warning(request, event)
        #     else:
        #         messages.warning(request, u'项目添加失败')
        #         return redirect('/wgsite/bmbsproject')

        # elif 'mark_done' in request.POST:
        #     del_list = request.POST.getlist('mark_done')

        #     models.BsProject.objects.filter(
        #         id__in=del_list).update(is_delete=True)
        #     messages.info(request, u'任务已经删除')

    else:
        form = forms.BsProForm()
    bmbsproject = models.BmBsProject.objects.filter(myuser__user__id=request.user.id)
    bsproject = models.BsProject.objects.all()
    return render(request, 'bmbsproject.html', locals())


def nofound(request):
    return render(request, '404.html')


def dcbsproject(request):
    itemid = request.GET.get('id', '')
    if request.method == 'POST':
        response = HttpResponse(content_type="application/ms-excel")
        response['Content-Disposition'] = 'attachment; filename="数据名单.xls"'
        wb = xlwt.Workbook()

        ws = wb.add_sheet(u'sheet1')
        ws.write(0, 0, u'姓名')
        ws.write(0, 1, u'邮箱')
        ws.write(0, 2, u'手机号码')
        ws.write(0, 3, u'性别')
        #ws.write(0, 4, u'身份证号码')
        row = 1
        bsproject = models.BmBsProject.objects.filter(bsproject_id=itemid)
        for i in bsproject:
            myuser = models.MyUser.objects.get(id=i.myuser_id)
            ws.write(row, 0, myuser.realname)
            ws.write(row, 1, myuser.user.email)
            ws.write(row, 2, myuser.phone_number)
            ws.write(row, 3, myuser.sex)
            row += 1
        wb.save(response)
        return response
    return render(request, 'bsproject.html', locals())

def abmbsproject(request):
    '''
    :param request:
    :return: 上传文件excel表格 ,并进行解析
    '''
    if request.method == "POST":
        print("post request")
        myform = forms.FileUploadForm(request.POST, request.FILES)

        #在这里可以添加筛选excel的机制
        if myform.is_valid():
            # print(myform)
            f = request.FILES['my_file']
            print(f)

            #开始解析上传的excel表格
            wb = xlrd.open_workbook(filename=None, file_contents=f.read())  # 关键点在于这里
            table = wb.sheets()[3]
            nrows = table.nrows  #行数
            ncole = table.ncols  #列数
            print("row :%s, cole: %s" % (nrows, ncole))

            for i in range(1, nrows):
                rowValues = table.row_values(i)  #一行的数据

                print(rowValues)
                zkzh = rowValues[0]
                realname = rowValues[1]
                email = rowValues[2]
                phone_number = rowValues[3]
                myuser = models.MyUser.objects.filter(realname= realname,phone_number=phone_number)
                if myuser:
                    myuser = myuser[0]
                    bsproject = models.BsProject.objects.get(id=1)
                    bmbsproject = models.BmBsProject.objects.filter(myuser = myuser,bsproject=bsproject)
                    if bmbsproject:
                        bmbsproject=bmbsproject[0]
                        bmbsproject.zkzh = zkzh
                        bmbsproject.save()
                    else:
                        messages.add_message(request, messages.WARNING, i+'行导入错误')
                else:
                    messages.add_message(request, messages.WARNING, i+'行导入错误')



                # pf = PhoneMsg.objects.filter(M_name = R_projectname)
                # # pf = PhoneMsg.objects.all()
                # if not pf.exists():   #空值
                #     return render(request,'abmbsproject.html',context={'error':u'R_projectname 不存在,联系管理员进行添加!'})

                # print(pf)

                # pm = PhoneMsg.objects.get(M_name =R_projectname)
                # pm.save()
                # re = Result()           #实例化result表
                # re.R_projectname = R_projectname
                # re.R_name = rowValues[2]
                # re.R_version = rowValues[3]
                # re.R_context = rowValues[4]
                # re.R_result = rowValues[5]
                # re.R_note = rowValues[6]
                # re.R_ower = rowValues[7]
                # re.R_kexuan = rowValues[8]
                # re.R_inning = rowValues[9]
                # re.R_createtime = datetime(*xldate_as_tuple(rowValues[10],0))
                # print(datetime(*xldate_as_tuple(rowValues[10],0)))
                # re.save()
                # pm.result.add(re)

            #handle_upload_file(f, str(f))        #上传文件处理
        myform = forms.FileUploadForm()
        return render(request, "abmbsproject.html", context={'form': myform, 'what': "文件传输"})


    else:
        print("get request")
        myform = forms.FileUploadForm()
        return render(request, 'abmbsproject.html', context={'form': myform, 'what': "文件传输"})

@login_required(login_url='/login/')
def showbm(request):
    bsproject = models.BmBsProject.objects.all()
    return render(request, 'showbm.html', locals())
def weibo(request):
    return render(request, 'weibo.html', locals())
def lbmbsproject(request):
    '''
    :param request:
    :return: 上传文件excel表格 ,并进行解析
    '''
    if request.method == "POST":
        print("post request")
        myform = forms.FileUploadForm(request.POST, request.FILES)

        #在这里可以添加筛选excel的机制
        if myform.is_valid():
            # print(myform)
            f = request.FILES['my_file']
            print(f)

            #开始解析上传的excel表格
            wb = xlrd.open_workbook(filename=None, file_contents=f.read())  # 关键点在于这里
            table = wb.sheets()[0]
            nrows = table.nrows  #行数
            ncole = table.ncols  #列数
            print("row :%s, cole: %s" % (nrows, ncole))

            for i in range(1, nrows):
                rowValues = table.row_values(i)  #一行的数据

                realname = rowValues[0]
                phone_number = rowValues[2]
                myuser = models.MyUser.objects.filter(realname= realname,phone_number=phone_number)
                if myuser:
                    myuser = myuser[0]
                    bsproject = models.BsProject.objects.get(id=1)
                    bmbsproject = models.BmBsProject.objects.filter(myuser = myuser,bsproject=bsproject)
                    if bmbsproject:
                        bmbsproject=bmbsproject[0]
                        bmbsproject.lqqk = 1
                        bmbsproject.save()
                    else:
                        messages.add_message(request, messages.WARNING, i+'行导入错误')
                else:
                    messages.add_message(request, messages.WARNING, i+'行导入错误')



                # pf = PhoneMsg.objects.filter(M_name = R_projectname)
                # # pf = PhoneMsg.objects.all()
                # if not pf.exists():   #空值
                #     return render(request,'abmbsproject.html',context={'error':u'R_projectname 不存在,联系管理员进行添加!'})

                # print(pf)

                # pm = PhoneMsg.objects.get(M_name =R_projectname)
                # pm.save()
                # re = Result()           #实例化result表
                # re.R_projectname = R_projectname
                # re.R_name = rowValues[2]
                # re.R_version = rowValues[3]
                # re.R_context = rowValues[4]
                # re.R_result = rowValues[5]
                # re.R_note = rowValues[6]
                # re.R_ower = rowValues[7]
                # re.R_kexuan = rowValues[8]
                # re.R_inning = rowValues[9]
                # re.R_createtime = datetime(*xldate_as_tuple(rowValues[10],0))
                # print(datetime(*xldate_as_tuple(rowValues[10],0)))
                # re.save()
                # pm.result.add(re)

            #handle_upload_file(f, str(f))        #上传文件处理
        myform = forms.FileUploadForm()
        return render(request, "lbmbsproject.html", context={'form': myform, 'what': "文件传输"})
    else:
        print("get request")
        myform = forms.FileUploadForm()
        return render(request, 'lbmbsproject.html', context={'form': myform, 'what': "文件传输"})

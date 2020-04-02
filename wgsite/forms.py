from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.widgets.TextInput(
        attrs={
            'class': 'form-control form-control-user',
            'placeholder': '用户名'
        }))
    password = forms.CharField(widget=forms.widgets.PasswordInput(
        attrs={
            'class': 'form-control form-control-user',
            'placeholder': '密码'
        }))


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.widgets.TextInput(
        attrs={
            'class': 'form-control form-control-user',
            'placeholder': '用户名（登录凭证）'
        }))
    email = forms.EmailField(widget=forms.widgets.TextInput(
        attrs={
            'class': 'form-control form-control-user',
            'type': 'email',
            'placeholder': '电子邮箱'
        }))
    password = forms.CharField(widget=forms.widgets.PasswordInput(
        attrs={
            'class': 'form-control form-control-user',
            'placeholder': '密码'
        }))
    repassword = forms.CharField(widget=forms.widgets.PasswordInput(
        attrs={
            'class': 'form-control form-control-user',
            'placeholder': '确认密码'
        }))


class WsxxModelForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['realname', 'sex', 'phone_number', 'college', 'weibo']
        exclude = []
        labels = {
            'realname': '真实姓名',
            'sex': '性别',
            'phone_number': '手机号码',
            'college': '所在院校',
            'weibo': '微博昵称'
        }
        widgets = {
            'realname':
            forms.widgets.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'True'
            }),
            'sex':
            forms.widgets.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'True',
            }),
            'phone_number':
            forms.widgets.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'True',
            }),
            'college':
            forms.widgets.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'True',
            }),
            'weibo':
            forms.widgets.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'True',
            }),
        }


class ChangeWsxxModelForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['realname', 'sex', 'phone_number', 'college']
        exclude = []
        labels = {
            'realname': '真实姓名',
            'sex': '性别',
            'phone_number': '手机号码',
            'college': '所在院校'
        }
        user_sex_choice = (
            ('男', u'男'),
            ('女', u'女'),
        )
        widgets = {
            'user':
            forms.widgets.HiddenInput(),
            'realname':
            forms.widgets.TextInput(attrs={
                'class': 'form-control',
            }),
            'sex':
            forms.widgets.Select(choices=user_sex_choice,
                                 attrs={
                                     'class': 'form-control',
                                 }),
            'phone_number':
            forms.widgets.TextInput(attrs={
                'class': 'form-control',
            }),
            'college':
            forms.widgets.TextInput(attrs={
                'class': 'form-control',
            }),
        }


class AddWsxxForm(forms.Form):
    user_sex_choice = (
        ('男', u'男'),
        ('女', u'女'),
    )
    realname = forms.CharField(
        widget=forms.widgets.TextInput(attrs={
            'class': 'form-control',
        }),
        label='真实姓名')
    sex = forms.ChoiceField(
        choices=user_sex_choice,
        widget=forms.widgets.Select(attrs={
            'class': 'form-control',
        }),
        label='您的性别')
    phone_number = forms.CharField(
        widget=forms.widgets.TextInput(attrs={
            'class': 'form-control',
        }),
        label='电话号码')
    college = forms.CharField(
        widget=forms.widgets.TextInput(attrs={
            'class': 'form-control',
        }),
        label='所在院校')


class AdminUserForm(forms.Form):
    def __init__(self, query_set=None, *args, **kwargs):
        super(AdminUserForm, self).__init__(*args, **kwargs)
        # user = forms.ModelMultipleChoiceField(label=u"用户:",
        #                                       required=False,
        #                                       widget=forms.CheckboxSelectMultiple,
        #                                       queryset=query_set)
        user_choice = (('', ''), )
        for temp in query_set:
            user_choice += ((temp['id'], temp['myuser__realname']), )

        user = forms.ChoiceField(
            choices=user_choice,
            widget=forms.widgets.Select(attrs={
                'class': 'form-control',
            }),
            label='用户')

        other = forms.CharField(
            widget=forms.widgets.TextInput(attrs={
                'class': 'form-control',
            }),
            label='备注',
            required=False,
        )
        self.fields['user'] = user
        self.fields['other'] = other


class AddAdminUserForm(forms.Form):
    user = forms.CharField(
        widget=forms.widgets.TextInput(attrs={
            'class': 'form-control',
        }),
        label='用户',
    )

    other = forms.CharField(
        widget=forms.widgets.TextInput(attrs={
            'class': 'form-control',
        }),
        label='备注',
        required=False,
    )


class StaffUserForm(forms.Form):
    def __init__(self, query_set=None, *args, **kwargs):
        super(StaffUserForm, self).__init__(*args, **kwargs)
        if query_set != None:
            user_choice = (('', ''), )
            for temp in query_set:
                user_choice += ((temp['id'], temp['realname']), )

            staff_user = forms.ChoiceField(
                choices=user_choice,
                widget=forms.widgets.Select(attrs={
                    'class': 'form-control',
                }),
                label='用户')
        else:
            staff_user = forms.CharField(
                widget=forms.widgets.Select(attrs={
                    'class': 'form-control',
                }),
                label='用户')
        department_choice = (
            ('理事会', u'理事会'),
            ('IT部', u'IT部'),
            ('财务部', u'财务部'),
            ('规培部-队长方向', u'规培部-队长方向'),
            ('规培部-教学方向', u'规培部-教学方向'),
            ('女童保护', u'女童保护'),
            ('水计划-教学方向', u'水计划-教学方向'),
            ('水计划-调研方向', u'水计划-调研方向'),
            ('宣传部', u'宣传部'),
            ('综合管理部-行政方向', u'综合管理部-行政方向'),
            ('综合管理部-人事方向', u'综合管理部-人事方向'),
            ('综合管理部-外事方向-高校社团合作', u'综合管理部-外事方向-高校社团合作'),
            ('综合管理部-外事方向-家访', u'综合管理部-外事方向-家访'),
            ('财务部', u'财务部'),
        )
        department = forms.ChoiceField(
            choices=department_choice,
            widget=forms.widgets.Select(attrs={
                'class': 'form-control',
            }),
            label='部门',
        )
        birthdate = forms.DateField(
            label='生日',
            widget=forms.widgets.TextInput(attrs={
                'class': 'form-control',
            }))
        staff_other = forms.CharField(
            widget=forms.widgets.DateInput(attrs={
                'class': 'form-control',
            }),
            label='备注',
            required=False,
        )
        self.fields['staff_user'] = staff_user
        self.fields['department'] = department
        self.fields['birthdate'] = birthdate
        self.fields['staff_other'] = staff_other


class BsProForm(forms.ModelForm):

    def __init__(self,  *args, **kwargs):
        super(BsProForm, self).__init__(*args, **kwargs)

    class Meta:
        model = BsProject
        exclude = []
        labels = {
            'name': '项目名称',
            'link': '易考链接',
            'able': '是否可以报名',
        }
        widgets = {
            'name':
            forms.widgets.TextInput(attrs={
                'class': 'form-control',
            }),
            'link':
            forms.widgets.TextInput(attrs={
                'class': 'form-control',
            }),
        }


class FileUploadForm(forms.Form):
    my_file = forms.FileField(widget=forms.widgets.FileInput(attrs={
        'class': 'form-control',
    }), label='文件名称:')

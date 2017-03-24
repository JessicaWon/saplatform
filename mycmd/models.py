from django.db import models
from django import forms
from datetime import datetime
from django.contrib.auth.models import User,Group
from guardian.shortcuts import assign_perm,assign,remove_perm
from guardian.models import UserObjectPermission

# Create your models here.

class userCmd(models.Model):
    u_cmd = models.CharField(max_length=50)
    def __unicode__(self):
        return str(self.u_cmd)

class userFile(models.Model):
    f_title = models.CharField(max_length = 30)
    u_file = models.FileField(upload_to = './upload/')
    def __unicode__(self):
        return self.f_title

class UserForm(forms.Form):
    username = forms.CharField()
    headImg = forms.FileField()

class CloudServerStatus(models.Model):
    update_time = models.DateTimeField(default=datetime.now)
    server_ip = models.CharField(max_length = 60)
    server_status = models.CharField(max_length = 60)
    server_status_reason = models.CharField(max_length = 60)
    engineer_name = models.CharField(max_length = 60)
    def __unicode__(self):
        return self.server_status
#----------------------------------------------------------------
class SaltUserFileForm(forms.Form):
    upload_file = forms.FileField()
    #update_dir = forms.CharField()
    salt_command = forms.CharField()
    #salt_host = forms.CharField(max_length = 50)
    ##server_list_data can change to ServerList.objects.all()
    #server_list_data = (("1","server1"),("2","server2"),("3","server3"))
    #server_list_data = CloudServerStatus.objects.all()
    #server_list = forms.MultipleChoiceField(choices=server_list_data,widget=forms.CheckboxSelectMultiple())
#class SaltUserFileForm(forms.Form):
#    upload_file = forms.FileField()
#    update_dir = forms.CharField()
#    salt_command = forms.CharField()
#    salt_host = forms.CharField(max_length = 50)

class SaltCommandMethod(forms.Form):
    salt_command_list = (("file update","cp.get_file"),("directory update","cp.get_dir"),("get file from a url","cp.get_url"))
    salt_command_select = forms.MultipleChoiceField(choices=salt_command_list,widget=forms.CheckboxSelectMultiple())


class SaltUserFile(models.Model):
    create_time = models.DateTimeField(default=datetime.now)
    update_time = models.DateTimeField(default=datetime.now)
    upload_file = models.FileField(upload_to = './upload/')
    #update_dir = models.CharField(max_length = 60)
    salt_command = models.CharField(max_length = 50)
    #salt_host = models.CharField(max_length = 50)
    def __unicode__(self):
        return self.salt_command
#-----------------------------------------------------------
class SaltUpdateFile(models.Model):
    create_time = models.DateTimeField(default=datetime.now)
    update_time = models.DateTimeField(default=datetime.now)
    engineer_name = models.CharField(max_length = 60)
    upload_file = models.FileField(upload_to = './upload/')
    update_dir = models.CharField(max_length = 60)
    project_name = models.CharField(max_length = 60)
    project_dir = models.CharField(max_length = 60)
    salt_command = models.CharField(max_length = 60)
    salt_selected_gameserver = models.CharField(max_length = 60)
    salt_outcome = models.CharField(max_length = 60)
    def __unicode__(self):
        return self.salt_outcome

class GameServer(models.Model):
    create_time = models.DateTimeField(default=datetime.now)
    update_time = models.DateTimeField(default=datetime.now)
    engineer_name = models.CharField(max_length = 60)
    project_name = models.CharField(max_length = 60)
    gameserver_id = models.CharField(max_length = 60)
    project_dir = models.CharField(max_length = 60)
#    salt_master = models.CharField(max_length = 60)
    cloud_server_eth0_ip = models.CharField(max_length = 60)
    def __unicode__(self):
        return self.gameserver_id

#class GameServerDir(models.Model) #still not decided whether to create this model
class LoginForm(forms.Form):
    username = forms.CharField(
            required = True,
            label = 'username',
            error_messages={'required':'please input username'},
            widget=forms.TextInput(
                attrs={
                    'placeholder':'Username',
                    'size': '40',
                    }
                )
            )

    password = forms.CharField(
            required=True,
            label = 'password',
            error_messages = {'required':'please input password'},
            widget=forms.PasswordInput(
                attrs={
                    'placeholder':'Password',
                    'size': '40',
                    }
                ),
            )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError('you should input username and password')
        else:
            cleaned_data = super(LoginForm,self).clean()

class UserDelList(models.Model):
    #def __init__(self,deleted_by,deleted_user_id,deleted_time,delete_result):
    deleted_by = models.CharField(max_length=32)
    deleted_user_id = models.ForeignKey(User)
    deleted_time = models.DateTimeField(default=datetime.now)
    delete_result = models.TextField()

    class Meta:
        permissions = (
            ("view_task", "Can see available tasks"),
        )

    def del_user_task(self):
        #print self.deleted_by
        #print "aaaaaa"
        if self.deleted_user_id != 1:
            user = User.objects.get(id=self.deleted_user_id_id)
            user.delete()
        else:
            return "could not delete super user"
        print "aaaaaa"


class Host(models.Model):
    hostname = models.CharField(max_length=64, unique=True)
    ip_addr = models.GenericIPAddressField(unique=True)
    port = models.IntegerField(default=22)
    system_type_choices = (
        ('linux', "Centos6"),
        ('linux', "Centos7")
    )
    system_type = models.CharField(choices=system_type_choices, max_length=32)
    enabled = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    online_date = models.DateTimeField()
    groups = models.ManyToManyField('HostGroup')
    service_company = models.ForeignKey('ServiceCompany')

    def __unicode__(self):
        return self.hostname


class ServiceCompany(models.Model):    # aws or aliyun
    name = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return self.name


class HostGroup(models.Model):  # host group
    name = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=64, unique=True)
    host_groups = models.ManyToManyField('HostGroup', blank=True, null=True)
    hosts = models.ManyToManyField('Host', blank=True, null=True)

    def __unicode__(self):
        return self.name

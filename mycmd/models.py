from django.db import models
from django import forms
from datetime import datetime
# Create your models here.

class userCmd(models.Model):
    u_cmd = models.CharField(max_length=50)
    def __unicode__(self):
        return str(self.u_cmd)

class userHost(models.Model):
    u_host = models.CharField(max_length=50)
    def __unicode__(self):
        return str(self.u_host)

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

#class CloudServerStatus(models.Model):
#    update_time = models.DateTimeField(default=datetime.now)
#    server_ip = models.CharField(max_length = 60)
#    server_status = models.CharField(max_length = 60)
#    server_status_reason = models.CharField(max_length = 60)
#    def __unicode__(self):
#        return self.server_status

#class GameServerDir(models.Model) #still not decided whether to create this model
class LoginForm(forms.Form):
    username = forms.CharField(
            required = True,
            label = 'username',
            error_messages={'required':'please input username'},
            widget=forms.TextInput(
                attrs={
                    'placeholder':'password',
                    }
                )
            )

    password = forms.CharField(
            required=True,
            label = 'password',
            error_messages = {'required':'please input password'},
            widget=forms.PasswordInput(
                attrs={
                    'placeholder':'password',
                    }
                ),
            )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError('you should imput username and password')
        else:
            cleaned_data = super(LoginForm,self).clean()


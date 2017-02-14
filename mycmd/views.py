#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import forms
from mycmd.models import userCmd,userHost,userFile,UserForm,SaltUserFile,SaltUserFileForm,LoginForm,GameServer,CloudServerStatus
#from mycmd.models import *
import os, urllib2, urllib, json, re, time, datetime, shutil
#import pickle
#from mycmd.config import *
from mycmd import salt_read_dir
import salt.client
import os
#import os
#import os.path
#import json
#from mycmd.salt_read_dir import *
# Create your views here.
class saltAPI:
    def __init__(self):
        self.__url = 'https://192.168.30.148:8000'
        self.__user =  'saltapi'           
        self.__password = 'woshishui'        
        self.__token_id = self.salt_login()

    def salt_login(self):
        params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
        encode = urllib.urlencode(params)
        obj = urllib.unquote(encode)
        headers = {'X-Auth-Token':''}
        url = self.__url + '/login'
        req = urllib2.Request(url, obj, headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        try:
            token = content['return'][0]['token']
            return token
        except KeyError:
            raise KeyError

    def postRequest(self, obj, prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token'   : self.__token_id}
        req = urllib2.Request(url, obj, headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        return content['return']
    def saltCmd(self, params):
        obj = urllib.urlencode(params)
        obj, number = re.subn("arg\d", 'arg', obj)
        res = self.postRequest(obj)
        return res

#sapi = saltAPI()
#testcmd = 'test.ping'
#
#params = {'client':'local', 'fun':testcmd, 'tgt':'*'}
#params = {'client':'local', 'fun':'test.ping', 'tgt':'*'}
#test = sapi.saltCmd(params)


def cmd(request):
    if request.method=='POST':

        u_file_frompage = UserForm(request.POST,request.FILES)

        if u_file_frompage.is_valid():
#            u_file = uf.cleaned_data['u_file']
            return HttpResponse('successully uploaded')
            username = form.cleaned_data['username']
            headImg = form.cleaned_data['headImg']

            file = userFile()
            file.f_title = username
            file.u_file = headImg
            file.save()
        #print username

        u_cmd_frompage = request.POST.get("u_cmd",'')
        print u_cmd_frompage
        p1 = userCmd(u_cmd = u_cmd_frompage)
        p1.save()

        u_host_frompage = request.POST.get("u_host",'')
        print u_host_frompage
        p2 = userHost(u_host = u_host_frompage)
        p2.save()
    #else
    #    u_file_frompage = userFile()
    return render(request,'index.html')
#    return render_to_response(request,'cmd.html',{'u_file_frompage':u_file_frompage}) #some problems               

#sapi = saltAPI()
#testcmd = userCmd.objects.filter(u_cmd="ping")

#params = {'client':'local', 'fun':testcmd, 'tgt':'*'}
#test = sapi.saltCmd(params)
def upload_file(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():

            username = form.cleaned_data['username']
            headImg = form.cleaned_data['headImg']

            print username
            print headImg
            file = userFile()
            file.f_title = username
            file.u_file = headImg
            file.save()
            return HttpResponse('uploaded successfully in upload function')

    else:
        form = userFile()
    return render_to_response('upload.html', {'form': form})


def update_file(request):
    if request.method == 'POST':
        form = SaltUserFileForm(request.POST, request.FILES)
        if form.is_valid():
            upload_file_page = form.cleaned_data['upload_file']
            update_dir_page = form.cleaned_data['update_dir']
            salt_command_page = form.cleaned_data['salt_command']
            salt_host_page = form.cleaned_data['salt_host']

            file = SaltUserFile()
            file.upload_file = upload_file_page
            file.update_dir = update_dir_page
            file.salt_command = salt_command_page
            file.salt_host = salt_host_page
            file.save()

            sapi = saltAPI()
            print sapi
            params = {'client':'local', 'fun':salt_command_page, 'tgt':'*'}
            print params
            u_result = sapi.saltCmd(params)
            print u_result
            html = "<html><body>It is now %s.</body></html>" %u_result


            return HttpResponse(html)
    else:
        form = SaltUserFile()
    return render_to_response('update.html', {'form': form})


## the following code is to list contents of directories in a tree-like format
def post_json_data_to_ztree(request):
#    jsonlist = []
    dirpath = '/opt'
    tmp_list = salt_read_dir.getfile(dirpath)
    return render_to_response('display.html', {'List': json.dumps(tmp_list)})

## over
## get all 
json_data ={}
def get_server_to_be_updated(request):
    if request.method == 'POST':
        ## if you donnot make json_data as a global parameter, then there is a error,and you should announce it before the function by"json_data = {}"
        global json_data
        json_data = request.POST['data']
        print '-------serverlist---',json_data,'-----------'
        #content = json.loads(json_data)
    else:
        return "post json data raised a error"
    #return json_data
        #var selected_server_list[];
## get all server list is over

## uploadfy
#@csrf_exempt  
#@requires_csrf_token
def uploadify_script(request):  
     if request.method == 'POST':
     
         files = request.FILES.getlist('uploadFile')
         print '--------------all files-----------',files[0]
         print '--------------all files-----------',files
         for f in files:
             print '----------file name-----------',f.name
             with open('/tmp/'+f.name,'wb+') as des:
                 for chunk in f.chunks():
                     des.write(chunk)
 
     return HttpResponse('upload successfully')  
  
def profile_upload(file):  
    '''''文件上传函数'''  
    if file:  
        path=os.path.join(settings.MEDIA_ROOT,'upload')  
        #file_name=str(uuid.uuid1())+".jpg"  
        file_name=str(uuid.uuid1())+'-'+file.name  
        #fname = os.path.join(settings.MEDIA_ROOT,filename)  
        path_file=os.path.join(path,file_name)  
        fp = open(path_file, 'wb')  
        for content in file.chunks():   
            fp.write(content)  
        fp.close()  
        return (True,file_name) #change  
    return (False,file_name)   #change  
  
#用户管理-添加用户-删除附件  
 
#@csrf_exempt  
#@requires_csrf_token
def profile_delte(request):  
    del_file=request.POST.get("delete_file",'')  
    if del_file:  
        path_file=os.path.join(settings.MEDIA_ROOT,'upload',del_file)  
        os.remove(path_file)
##uploadfy over
## update some files by select some directories
def update_files_salt(request):
    data_array = ""
    client = salt.client.LocalClient()
    ## the all_dir is the json format, if need dict format, we need to translate all ''to ""
    all_dir = client.cmd('*', 'cmd.run', ['python /srv/salt/pathtreeview.py'])
    data_array_length = len(all_dir.values())
    print '---type--',type(all_dir.values()), '----type---'
    for i in range(data_array_length):
        data_array = all_dir.values()[i] + data_array
    ## there is no need to translate data_array to data array json format
    data_array = dict = str(data_array).replace('][',',')
    print '------data-array---',data_array,'---------'
    if request.method == 'POST':
        form = SaltUserFileForm(request.POST,request.FILES)
        if form.is_valid():
            #upload_file = form.cleaned_data['upload_file']
            upload_file1 = request.FILES.getlist('uploadFile')
            print '--|||||||||||||||||||||||||---multi files-------',upload_file1
            ##for i in upload_file
            ##    dist_dir = open('/tmp/' + f.name,'wb+')
            ##    print i
            ##    for chunk in f.chunks():
            ##        dist_dir.write(chunk)
            ##    dist_dir.close()
            #update_dir = form.cleaned_data['update_dir']
            salt_command = form.cleaned_data['salt_command']
            print '`````````````````````',salt_command
            #salt_host = form.cleaned_data['salt_host']

            content = json.loads(json_data)
            content1 = content[1]
            server_length = len(content)


            file = SaltUserFile()
            file.upload_file = upload_file
            #file.update_dir = update_dir
            file.salt_command = salt_command
            #file.salt_host = salt_host
            file.save()
            ## when you want to distract file name from your path, you need to translate it to str first, or it will occur error
            file_name_str = str(file.upload_file)
            ## os.path.basename can be used to get rid of path dir to get filename, it needs to import os
            file_name = os.path.basename(file_name_str)
##            file_abs_dir = '/usr/local/src/cmdb/saltcmd/upload/'+ file_name
            file_abs_dir = '/tmp/'+ file_name
            os.path.exists(file_abs_dir)
            shutil.move(file_abs_dir ,"/srv/salt/")
            srcsaltfiledir = 'salt://' + file_name

            # every gameserver which in every server need to be updated
            for x in range(server_length):
                if True in content[x].values():
                    physical_server = content[x]["name"]
                    gameserver_length = len(content[x]["children"])
                    for y in range(gameserver_length):
                        if True in content[x]["children"][y].values():
                            gameserver_list = content[x]["children"][y]["name"]
                            distsaltfiledir = '/opt/' + gameserver_list + '/' + file_name
                            print distsaltfiledir
                            ret = client.cmd(physical_server,salt_command,[srcsaltfiledir,distsaltfiledir])
                        else:
                            pass
                    
            ## ret = client.cmd('*','cp.get_file',[srcsaltfiledir,distsaltfiledir])
            
            return HttpResponse('uploaded successfully in upload function')
    else:
        form = SaltUserFileForm() #初始化空表单
    return render_to_response('display.html', {'form': form,'List': data_array})

def get_server_status(request):
##    infors = list()
    results = CloudServerStatus.objects.all()
    print results
    return render_to_response('general.html', {'results': results})

def index_page(request):  
    context = {}

    ## get the recent six months' name to display and to be used in following code
    today_date = datetime.date.today()
    this_month = today_date.strftime("%B")

    firstday_this_month = today_date.replace(day=1)
    lastday_last_month = firstday_this_month - datetime.timedelta(days=1)
    last_month = lastday_last_month.strftime("%B")    

    firstday_last_month = lastday_last_month.replace(day=1)
    lastday_two_months_ago = firstday_last_month - datetime.timedelta(days=1)
    two_months_ago = lastday_two_months_ago.strftime("%B")

    firstday_two_months_ago =lastday_two_months_ago.replace(day=1)
    lastday_three_months_ago = firstday_two_months_ago - datetime.timedelta(days=1)
    three_months_ago = lastday_three_months_ago.strftime("%B")

    firstday_three_months_ago = lastday_three_months_ago.replace(day=1)
    lastday_four_months_ago = firstday_three_months_ago - datetime.timedelta(days=1)
    four_months_ago = lastday_four_months_ago.strftime("%B")

    firstday_four_months_ago = lastday_four_months_ago.replace(day=1)
    lastday_five_months_ago = firstday_four_months_ago - datetime.timedelta(days=1)
    five_months_ago = lastday_five_months_ago.strftime("%B")

    firstday_five_months_ago = lastday_five_months_ago.replace(day=1)
    lastday_six_months_ago = firstday_five_months_ago - datetime.timedelta(days=6)
    six_months_ago = lastday_six_months_ago.strftime("%B")

    firstday_six_months_ago = lastday_six_months_ago.replace(day=1)
    month_name_pool = [six_months_ago,five_months_ago,four_months_ago,three_months_ago,two_months_ago,last_month,this_month]
    print month_name_pool

    ## distract data from MySQL to display
    ## new purchased cloud server account in each month
    new_cloud_server_this_month = CloudServerStatus.objects.filter(update_time__gt=firstday_this_month).count()
    new_cloud_server_last_month = CloudServerStatus.objects.filter(update_time__lt=firstday_this_month,update_time__gt=firstday_last_month).count()
    new_cloud_server_two_months_ago = CloudServerStatus.objects.filter(update_time__lt=firstday_last_month,update_time__gt=firstday_two_months_ago).count()
    new_cloud_server_three_months_ago = CloudServerStatus.objects.filter(update_time__lt=firstday_two_months_ago,update_time__gt=firstday_three_months_ago).count()
    new_cloud_server_four_months_ago = CloudServerStatus.objects.filter(update_time__lt=firstday_three_months_ago,update_time__gt=firstday_four_months_ago).count()
    new_cloud_server_five_months_ago = CloudServerStatus.objects.filter(update_time__lt=firstday_four_months_ago,update_time__gt=firstday_five_months_ago).count()
    new_cloud_server_six_months_ago = CloudServerStatus.objects.filter(update_time__lt=firstday_five_months_ago,update_time__gt=firstday_six_months_ago).count()
    new_cloud_server_half_year = [new_cloud_server_six_months_ago,new_cloud_server_five_months_ago,new_cloud_server_four_months_ago,new_cloud_server_three_months_ago,new_cloud_server_two_months_ago,new_cloud_server_last_month,new_cloud_server_this_month]
    print new_cloud_server_half_year

    ## new created game server account in each month
    new_game_server_this_month = GameServer.objects.filter(update_time__gt=firstday_this_month).count()
    new_game_server_last_month = GameServer.objects.filter(update_time__lt=firstday_this_month,update_time__gt=firstday_last_month).count()
    new_game_server_two_months_ago = GameServer.objects.filter(update_time__lt=firstday_last_month,update_time__gt=firstday_two_months_ago).count()
    new_game_server_three_months_ago = GameServer.objects.filter(update_time__lt=firstday_two_months_ago,update_time__gt=firstday_three_months_ago).count()
    new_game_server_four_months_ago = GameServer.objects.filter(update_time__lt=firstday_three_months_ago,update_time__gt=firstday_four_months_ago).count()
    new_game_server_five_months_ago = GameServer.objects.filter(update_time__lt=firstday_four_months_ago,update_time__gt=firstday_five_months_ago).count()
    new_game_server_six_months_ago = GameServer.objects.filter(update_time__lt=firstday_five_months_ago,update_time__gt=firstday_six_months_ago).count()
    new_game_server_half_year = [new_game_server_six_months_ago,new_game_server_five_months_ago,new_game_server_four_months_ago,new_game_server_three_months_ago,new_game_server_two_months_ago,new_game_server_last_month,new_game_server_this_month]
    print new_game_server_half_year

    ## other overview data displayed in the index page
    cloud_server = CloudServerStatus.objects.all().count()
    game_server = GameServer.objects.all().count()
    pkq_gameserver = GameServer.objects.filter(project_name='pkq').count()
    wlwz_gameserver = GameServer.objects.filter(project_name='wulinwaizhuan').count()
    sanguo_gameserver = GameServer.objects.filter(project_name='sanguo').count()
    other_gameserver = GameServer.objects.all().count() - pkq_gameserver - wlwz_gameserver - sanguo_gameserver

    ## get zabbix alert data by zabbix's api
    zabbix_alert = 1

    ## budget and payment in purchasing cloud servers
    turnover = 760

    ## it depends if all the users need this
    online_players = 2000000

    return render_to_response('index2.html', {'game_server':game_server,'cloud_server':cloud_server,'pkq_gameserver':pkq_gameserver,'wlwz_gameserver':wlwz_gameserver,'sanguo_gameserver':sanguo_gameserver,'other_gameserver':other_gameserver,'zabbix_alert':zabbix_alert,'turnover':turnover,'online_players':online_players,'pkq_data': pkq_gameserver,'month_name_pool':month_name_pool,'new_cloud_server_half_year':json.dumps(new_cloud_server_half_year),'new_game_server_half_year':json.dumps(new_game_server_half_year)})

def user_login(request):
    if request.method == 'GET':
        print 'request method is get'
        form = LoginForm()
        return render_to_response('login.html',{'form':form})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username','')
            password = request.POST.get('password','')
            print 'request method is post'
            print password
            user = auth.authenticate(username=username,password=password)
            if user is not None and user.is_active:
                auth.login(request,user)
                return HttpResponseRedirect('/login/')
            else:
                return render_to_response('login.html',{'form':form,'password_is_wrong':True})
        else:
            return render_to_response('login.html',{'form':form})


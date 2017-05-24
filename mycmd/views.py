#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import forms
from mycmd.models import userCmd,userFile,UserForm,SaltUserFile,SaltUserFileForm,LoginForm,GameServer,CloudServerStatus,SaltCommandMethod,UserDelList,UpdateFiles,UpdateFilesDB,GamesvList,InputDir
#from mycmd.models import *
import os, urllib2, urllib, json, re, time, datetime, shutil
#import pickle
#from mycmd.config import *
from mycmd import salt_read_dir
import salt.client
import salt.runner #show results
import os
from django.contrib.auth import authenticate
from django.contrib.auth.models import User,Group
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

import ConfigParser
from ldap3 import Server, Connection, SUBTREE
from ldap3 import HASHED_SALTED_SHA256
from ldap3.utils.hashed import hashed
from passlib.hash import ldap_md5_crypt as md5encode
from django.template import RequestContext

import crypt
import subprocess

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission
from guardian.shortcuts import assign_perm,assign
from guardian.models import UserObjectPermission
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.http import StreamingHttpResponse
import random
import time
from zipfile import * 
import zipfile

#import os
#import os.path
#import json
#from mycmd.salt_read_dir import *
# Create your views here.

file_name_list = []
@login_required(login_url="/login/")
def uploadify_script(request):
    if os.path.exists('/tmp/django_tmp/'):
        #os.system('rm -rf /tmp/django_tmp/*')
        pass
    else:
        os.mkdir('/tmp/django_tmp/')

    uploadfilename = []
    if request.method == 'POST':
        files = request.FILES.getlist('uploadFile')
        for f in files:
            file_name_list.append(f.name)
            tmpname = '<label id="showFile" name="showFile" class="badge bg-light-grey" font size="3" color="black">' + f.name + '</label></br>'
            #tmpname = f.name
            uploadfilename.append(tmpname)
            with open('/tmp/'+'/django_tmp/'+ f.name,'wb+') as des:
                for chunk in f.chunks():
                    des.write(chunk)
    response_data = {}
    perm_all = Permission.objects.all()

    return HttpResponse(uploadfilename)
    '''return rendertoresponse '''
    #return render_to_response('display.html', {'filenames': uploadfilename,'perm_all':perm_all},context_instance=RequestContext(request))
'''必须将后缀名写成一致的，因为如果一个带/，一个不带，那导致后面在对比的时候出现问题'''
def cmp_dir(dir1,dir2):
    #if os.path.isdir(dir1):
    status = []
    def get_dir_return(rootDir):
        absdirs = []
        dirs = []
        def Test2(rootDir):
            for lists in os.listdir(rootDir):
                newdir = os.path.join(rootDir, lists)
                if os.path.isdir(newdir):
                    #print newdir
                    absdirs.append(newdir)

                    Test2(newdir)
                else:
                    pass
                    #print 'no dir'
        #print dirs

        #print dirs
        thedir = rootDir
        length = len(thedir)
        Test2(thedir)
        for dir in absdirs:
            dirs.append(dir[length:])
        return dirs
    if os.path.isdir(dir1) and os.path.isdir(dir2):
        dir1list = get_dir_return(dir1)
        #print dir1list
        dir2list = get_dir_return(dir2)
        #print dir2list
        for filename in dir1list:
            if filename in dir2list:
                status.append(True)
            else:
                status.append(False)
        if all(status):
            return "True"
        else:
            return "False"
    else:
        return "error"
'''解压zip文件 '''
def un_zip(file_name,tmpdir):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(file_name)
    if os.path.isdir(tmpdir):
        pass
    else:
        os.mkdir(tmpdir)
    for names in zip_file.namelist():
        zip_file.extract(names,tmpdir)
    zip_file.close()
    #os.remove(file_name)

'''统计目录中的所有文件并且进行归类'''
def sortfile(rootDir):
    all_files = []
    config_files = []
    beam_files = []

    for root,dirs,files in os.walk(rootDir):
        for filespath in files:
            #print os.path.join(root,filespath)
            print filespath
            if os.path.splitext(filespath)[1][1:] == 'config':
                config_files.append(filespath)
                print config_files
            elif os.path.splitext(filespath)[1][1:] == 'beam':
                beam_files.append(filespath)
            else:
                pass
    all_files = {'config_files':config_files,'beam_files':beam_files}
    print all_files
    return all_files



@login_required(login_url="/login/")
@permission_required('mycmd.delete_userdellist')
def update_files_salt(request):
#    os.system('rm -rf /tmp/django_tmp/*')
    #create_dir = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    #print os.mkdir('/tmp/' + create_dir)
    length = len(file_name_list)
    for i in range(length):
        file_name_list.pop()
    ## the all_dir is the json format, if need dict format, we need to translate all ''to ""

    if request.method == 'POST':
        perm_all = Permission.objects.all()

        update = UpdateFilesDB(request.POST)
        create_dir = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
        print os.mkdir('/data/upload/' + create_dir)

        files = os.listdir('/tmp/django_tmp/')
        for file in files:
            shutil.move('/tmp/django_tmp/'+file ,"/data/upload/" + create_dir)

        files = os.listdir("/data/upload/" + create_dir)
        config_files = list()
        beam_files = list()
        zip_files = list()

        '''遍历文件，将文件复制到特定的目录|暂时不用这种方法来搬移文件了，使用上传zip包的方法来直接进行更新，但是会多出一个解压和统计文件夹中文件的函数,用于后面统计'''
        for afile in files:
            if zipfile.is_zipfile("/data/upload/" + create_dir + '/' + afile):
                zip_files.append(afile)
            elif os.path.splitext(afile)[1][1:] == 'config':
                config_files.append(afile)
                '''if afile == 'data_box.config':
                    shutil.copyfile('/data/upload/' + create_dir + '/' + afile, "/root/rsync/gameserver/config/moduleconfig/" + afile)
                else:
                    shutil.copyfile('/data/upload/' + create_dir + '/' + afile, "/root/rsync/gameserver/config/activityconfig/" + afile)'''
            elif os.path.splitext(afile)[1][1:] == 'beam':
                beam_files.append(afile)
                '''shutil.copyfile('/data/upload/' + create_dir + '/' + afile, "/root/rsync/gameserver/ebin/" + afile)'''
            else:
                pass
        print '---------------------config file---------------',config_files
        print '---------------------beam file---------------',beam_files
        print '---------------------zip file---------------',zip_files
        '''上传的文件分类'''
        uploadfiles = config_files + beam_files


        '''获取页面输入的所有数据,从上到下依次得到数据'''
        upload_dir = 'config/moduleconfig'
        is_all_gameserver = request.POST.get('all_gameserver')
        exclu_gameserver_id = request.POST.get('exclu_gameserver')
        input_gameserver_id = request.POST.get('input_gameserver')
        '''这个地方得到的数据是所有按钮的状态，如果on那就是点击状态，如果不是on那就不是点击状态,默认为至少一个on状态，如果是空的话返回错误'''
        operate_type = request.POST.getlist('updatename')
        operate_aim = request.POST.get('types')

        print '显示所有的输入',uploadfiles,is_all_gameserver,exclu_gameserver_id,input_gameserver_id,operate_type,operate_aim,upload_dir
        '''对输入的内容转化成数组形式'''
        input_servers= str(input_gameserver_id)
        exclu_gameserver = str(exclu_gameserver_id)
        '''输入的游戏服'''
        inputgmsvlist = input_servers.split(",")
        exclu_gameserver_id = exclu_gameserver.split(",")
        print exclu_gameserver_id


        '''判断上传文件中是否包含zip文件，或者包含多少个zip文件'''
        if len(zip_files) == 0:
            if len(uploadfiles) == 0:
                error_code = '更新文件夹中无有效文件，请重新上传'
                return render_to_response('error.html',{'errorcode':error_code},context_instance=RequestContext(request))
            else:
                if upload_dir == None:
                    error_code = '请输入上传文件目录'
                    return render_to_response('error.html',{'errorcode':error_code},context_instance=RequestContext(request))
                else:
                    new_tmp_dir = '/data/upload/' + create_dir + '/' + upload_dir
                    rysnc_from_dir = '/data/upload/' + create_dir
                    print 'rysnc_from_dir-----------',rysnc_from_dir,uploadfiles,new_tmp_dir
                    os.makedirs(new_tmp_dir)
                    for afiles in uploadfiles:
                        shutil.move( '/data/upload/' + create_dir + '/' + afile, rysnc_from_dir + '/' + upload_dir + '/' + afile)
        elif len(zip_files) == 1:
            if len(uploadfiles) == 0:
                upload_dir = '/'
                azipfile = zip_files[0]
                un_zip('/data/upload/' + create_dir + '/' + azipfile, '/data/upload/' + create_dir + '/')
                rysnc_from_dir = '/data/upload/' + create_dir + '/' + os.path.splitext(azipfile)[0] + '/'
                print rysnc_from_dir
                '''解压后的目录与原目录进行对比，如果对比正确，就统计里面的配置文件config和beam，接着同步或者更新；如果对比不成功，就返回错误信息进行提示zip文件中的文件目录不正确'''
                cpm_result = cmp_dir(rysnc_from_dir + '/', '/root/rsync/gameserver/')
                if cpm_result == "True":
                    pass
                else:
                    error_code = '压缩文件中的目录与rsync源文件夹不同'
                    return render_to_response('error.html',{'errorcode':error_code},context_instance=RequestContext(request))
                '''统计zip包中的config和beam文件'''
                sortoutcome = sortfile('/data/upload/' + create_dir)
                config_files = []
                beam_files = []
                config_files = sortoutcome['config_files']
                beam_files = sortoutcome['beam_files']
                uploadfiles = config_files + beam_files
            else:
                error_code = '上传文件中既包含zip又包含普通文件'
                return render_to_response('error.html',{'errorcode':error_code},context_instance=RequestContext(request))
        else:
            error_code = '上传文件中有多个zip包，请检查上传的文件'
            return render_to_response('error.html',{'errorcode':error_code},context_instance=RequestContext(request))

        '''判断上传文件的个数，如果大于1个就返回报错'''
        '''上传zip包进行解压到相应的目录，并进行解压'''
        '''解压后的目录与原目录进行对比，如果对比正确，就统计里面的配置文件config和beam，接着同步或者更新；如果对比不成功，就返回错误信息进行提示zip文件中的文件目录不正确'''
        '''上传后的文件与rsync中的文件进行同步'''
        rsync_command = "/usr/bin/rsync -vau --progress " + rysnc_from_dir + "/" + " " + "/root/rsync/gameserver/" + upload_dir + '/'
        #rsync_command = "/usr/bin/rsync -vau --progress" + " " + "/data/upload/" + create_dir + "/ " + "/root/rsync/gameserver/"
        print 'rsync command-----',rsync_command
        outcome = subprocess.Popen(rsync_command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print outcome

        '''判断更新文件夹中是否有文件,这个程序直接在前面的大的里面判断了，因为包含了zip文件，不用再次判断了'''
        '''if uploadfiles:
            pass
        else:
            error_code = '更新文件夹中无文件，请重新上传'
            return render_to_response('error.html',{'errorcode':error_code},context_instance=RequestContext(request))'''

        '''判断是否全选游戏服'''
        if is_all_gameserver == "all_gameserver":
            is_all_gameserver_status = "Yes"
            input_gameserver_id = "all gameservers"
        else:
            if input_gameserver_id:
                is_all_gameserver_status = "No"
            else:
                #return render_to_response('error.html')
                error_code = '请选择全服或者输入区服id'
                return render_to_response('error.html',{'errorcode':error_code},context_instance=RequestContext(request))

        '''判断同步或更新有无被选中'''
        if len(operate_type) == 0:
            #return render_to_response('error.html')
            error_code = '同步或者更新操作至少选择一个'
            return render_to_response('error.html',{'errorcode':error_code},context_instance=RequestContext(request))
        else:
            pass

        '''判断提交的操作目的有没有选择'''
        if operate_aim:
            pass
        else:
            #return render_to_response('error.html')
            error_code = '没有选择此次操作目的'
            return render_to_response('error.html',{'errorcode':error_code},context_instance=RequestContext(request))

        '''判断是同步还是更新操作'''
        if len(operate_type) == 1:
            manage_type = 'sync'
            client = salt.client.LocalClient()
            client.cmd('*','saltutil.sync_modules')
            result_jid = client.cmd_async('*','rsyncgmsv.syncgmfile',[exclu_gameserver_id,inputgmsvlist,is_all_gameserver_status,uploadfiles]) #rsyncfiles

        elif len(operate_type) == 2:
            manage_type = 'update'
            client = salt.client.LocalClient()
            client.cmd('*','saltutil.sync_modules')
            print '-------all parameters------',exclu_gameserver_id,inputgmsvlist,is_all_gameserver_status,uploadfiles
            result_jid = client.cmd_async('*','updategmsv.updategm',[exclu_gameserver_id,inputgmsvlist,is_all_gameserver_status,uploadfiles]) #updatefiles
        else:
            error_code = '既不是同步操作也不是更新'
            return render_to_response('error.html',{'errorcode':error_code},context_instance=RequestContext(request))

        opts = salt.config.master_config('/etc/salt/master')
        runner = salt.runner.RunnerClient(opts)
        #print runner.cmd('jobs.lookup_jid', [str(rsync_jid)])
        #result = client.cmd('*','updategmsv.updategm',[exclu1,inclu1,if_all_server1,uploadfiles1]) '''测试数据'''
        #run_rsync = client.cmd_async('*','cmd.script',['/usr/local/src/rsync.sh'])
        #print runner.cmd('jobs.lookup_jid', [str(run_rsync)])

        user_id = request.session.items()[1][1]
        username = User.objects.get( id = user_id )

        update = UpdateFilesDB()
        update.is_all_gameservers = is_all_gameserver_status
        update.input_gameserver_id = inputgmsvlist
        update.exclu_gameserver_id = exclu_gameserver_id
        update.update_type = manage_type
        update.update_by = username
        update.update_files_dir = '/data/upload/' + create_dir
        update.update_files = uploadfiles
        update.update_outcome = 'progressing'
        update.result_jid = result_jid
        update.update_fail_server = 'progressing'
        update.update_fail_details = 'progressing'
        update.save()

        ret = {"result_jid":result_jid}
        ret_json = json.dumps(ret)
        return HttpResponse(ret_json)

    else:
        #input_dir = InputDir()
        update = UpdateFilesDB()
        shutil.rmtree('/tmp/django_tmp/')
        os.mkdir('/tmp/django_tmp/')
        result_jid = None
        #return render_to_response('display.html', {'perm_all':perm_all,'username':username,'result_jid':result_jid},context_instance=RequestContext(request))


        #update_log = UpdateFilesDB.objects.order_by('-update_time')[:10]
        perm_all = Permission.objects.all()
        user_id = request.session.items()[1][1]
        print user_id
        username = User.objects.get( id = user_id )

        #return render_to_response('display.html', {'form': update,'outcomes':update_log,'perm_all':perm_all},context_instance=RequestContext(request))
        return render_to_response('display.html', {'perm_all':perm_all,'username':username,'result_jid':result_jid},context_instance=RequestContext(request))
        ## dump data to the html
        '''ret = {"result_jid":result_jid}
        ret_json = json.dumps(ret)'''
        '''return {'finishedgmsv':finishedgmsv,'allgmsv':allgmsv}'''
        #return HttpResponse(ret_json)
    '''else:
        update = UpdateFilesDB()
        shutil.rmtree('/tmp/django_tmp/')
        os.mkdir('/tmp/django_tmp/')
        result_jid = None
        perm_all = Permission.objects.all()
        return render_to_response('display.html', {'perm_all':perm_all,'username':username,'result_jid':result_jid},context_instance=RequestContext(request))'''





#@permission_required('mycmd.delete_userdellist')
@login_required(login_url="/login/")
def get_server_status(request):
##    infors = list()
    #results = CloudServerStatus.objects.all()
    print '---------session---------',request.session.items(),request.session,'------------'
    user_id = request.session.items()[1][1]
    print user_id
    username = User.objects.get( id = user_id )
    print '--------get username-------',username
    #results = CloudServerStatus.objects.filter( engineer_name = username)
    results = GamesvList.objects.all()
    print '--------get results-------',results
    print results
    return render_to_response('general.html', {'results': results})

@login_required(login_url="/login/")
def index_page(request):
#    if username != 'test@skymoons.com':
#        raise Exception("Please login frist")
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
    zabbix_alert = random.randint(0, 15)

    ## budget and payment in purchasing cloud servers
    turnover = 760

    ## it depends if all the users need this
    online_players = random.randint(20, 1500)

    user_id = request.session.items()[1][1]
    print user_id
    username = User.objects.get(id = user_id )


    return render_to_response('index2.html', {'username':username,'game_server':game_server,'cloud_server':cloud_server,'pkq_gameserver':pkq_gameserver,'wlwz_gameserver':wlwz_gameserver,'sanguo_gameserver':sanguo_gameserver,'other_gameserver':other_gameserver,'zabbix_alert':zabbix_alert,'turnover':turnover,'online_players':online_players,'pkq_data': pkq_gameserver,'month_name_pool':month_name_pool,'new_cloud_server_half_year':json.dumps(new_cloud_server_half_year),'new_game_server_half_year':json.dumps(new_game_server_half_year)})

def user_login(request):
    if request.method == 'GET':
        print 'request method is get'
        form = LoginForm()
        return render_to_response('login.html',{'form':form})
    else:
        print 'request method is post'
        form = LoginForm(request.POST)
        print form
        if form.is_valid():
            username = request.POST.get('username')
            #username = 'wangjuan@wangjuan'
            password = request.POST.get('password')
            #password = 'wangjuan'
            print 'get username and password succeefullly'
            print password
            ##create new users for test=====
            ## user = User.objects.create_user(username,username,password)
            ## user.last_name = 'test00000'
            ## user.save()
            ## create user end=====

            user = authenticate(username=username,password=password)
            print '----user----',user,'--------------'
            if user is not None and user.is_active:
                auth_login(request,user)
                print 'username or password is right'
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
                    print 'Youre logged in.'
                else:
                    print 'didnt get session'
                return HttpResponseRedirect('/index/')
            else:
                print 'username or password is wrong'
                return render_to_response('login.html',{'form':form,'password_is_wrong':True})
        else:
            username = request.POST.get('username','')
            #username = 'wangjuan@wangjuan'
            password = request.POST.get('id_password','')
            #password = 'wangjuan'
            if not username:
                print 'Enter a username.'
            print 'username and password is wrong'
            print password
            return render_to_response('login.html',{'form':form})
def user_logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/login/')


@login_required(login_url="/login/")
def user_management(request):
    results = User.objects.all()
    print '---------session---------',request.session.items(),'------------'
    print results
    aaa = "aaa"
    bbb = "111"
    title = "add a new user"
## use ldap to authorise
## read config files
##     total_entries = 0
##     conf = ConfigParser.SafeConfigParser()
##     conf.read('/usr/local/src/cmdb/saltcmd/mycmd/ldap.conf')
##     sections = conf.sections()
##     ldap_server = conf.get("ldap","server")
##     print '----------ldap server------',ldap_server
##     ldap_admin_user = conf.get("ldap", "admin_user")
##     ldap_pass = conf.get("ldap", "pass")
##     ldap_dn = conf.get("ldap", "dn")
## 
## ## connect to servers
##     server = Server(ldap_server)
##     conn = Connection(server,ldap_admin_user, ldap_pass, auto_bind=True)
##     conn.bind()
##     conn.search('ou=Services,dc=ldap,dc=skymoons,dc=com', '(objectclass=top)')
##     print '-------response---------',conn.response[0]['dn']
##     #print '-------single response-------',conn.response[0]['dn']
##     user_list = []
##     for i in conn.response:
##         print i['dn']
##         user_list.append(i['dn'])
##     print user_list
    group_all = Group.objects.all()
    session_role_id = 2
    return render_to_response('user.html', {'results': results,'group_all': group_all,'session_role_id':session_role_id},context_instance=RequestContext(request))

@login_required(login_url="/login/")
#@privileges_required
def user_add(request):
    if request.method == 'GET':
        print 'request method is get'
        #form = LoginForm()
        form = User()
        group_all = Group.objects.all()
        return render_to_response('user_add.html',{'form':form,'group_all': group_all},context_instance=RequestContext(request))
    else:
        ## try:
        ## first step is to add user to the login system which is in MySQLdb, second step is to add user to ldap DB
        username = request.POST.get('username')
        print '---------username------',username
        password = request.POST.get('password')
        print password
        email = request.POST.get('email')
        user = User.objects.create_user(username,email,password)
        user.last_name = username
        group = request.POST.get('groups')
        print '-------groupid------',group

        ## add user to the selected group
        user.groups.add(group)
        user.save()
        ## the second step is to add users to ldap
        #read ldap config file
        '''conf = ConfigParser.SafeConfigParser()
        conf.read('/usr/local/src/cmdb/saltcmd/mycmd/ldap.conf')
        ldap_server = conf.get("ldap","server")
        ldap_admin_user = conf.get("ldap", "admin_user")
        ldap_pass = conf.get("ldap", "pass")
        ldap_dn = conf.get("ldap", "dn")

        #connect to servers
        server = Server(ldap_server)
        conn = Connection(server,ldap_admin_user, ldap_pass, auto_bind=True)
        conn.bind()

        user_dn = 'uid=' + username + ',' + 'ou=People,ou=privileges,' + ldap_dn
        print user_dn
        ## every user has a unique number for uid
        uidnumber = 66
        add_type = ['inetOrgPerson','posixAccount','top']
        homedir = '/home/' + username
        ## hash the password to
        password1 = password.encode("utf-8")
        ## hashed password cannot be used in Unix, so we should use md5
        #hashed_password = hashed(HASHED_SALTED_SHA256, password1)
        #print '-----hashed password------',hashed_password

        md5_password = md5encode.encrypt(password1)
        print '----md5ed password---',md5_password
        attributes = {'givenName': username,'uid':username,'loginShell':'/bin/bash','userPassword':md5_password,'sn': 'yunwei','cn' : 'yunwei','uidNumber':uidnumber,'gidNumber':5044,'homeDirectory':homedir}
        conn.add(user_dn,add_type,attributes)
        ## use test to add a new user
        ##conn.add('uid=test12,ou=People,ou=privileges,dc=ldap,dc=skymoons,dc=com',['inetOrgPerson','posixAccount','top'],{'givenName': 'test12','uid':'test12','loginShell':'/bin/bash','userPassword':'{CRYPT}$6$PaQp4cLy$vVF.jvW71lnQgWg3FwfWs/mpu54cTlLxw2.Q29eZl6PhEVI6up.Pa35IVocDqmMyQpC/46eBqBqoF8wdMcp/G0','sn': 'won','cn' : 'won','uidNumber':62,'gidNumber':5044,'homeDirectory':'/home/test12'})
        ##print(conn.result)
        conn.unbind()
        print 'add user successfully'
        #return HttpResponseRedirect('/useradd/')'''
        return render_to_response('user_add.html',context_instance=RequestContext(request))
        #except:
        #    return HttpResponseRedirect('plz check your username and password')

@login_required(login_url="/login/")
#@permission_required('view.user_add')
def user_list(request):
    session_role_id = 2
    group_all = Group.objects.all()
    print group_all
    user_all = User.objects.all()
    print '------------user all---------',user_all
    #user = User.objects.get(id=45)
    #print '------------group all--------',user
    #print '--------------users group------', user.groups.through.get()
    #user_group = User.groups.objects.all()
    #print user_group
    
    #print 'wangjuans all perms -------',User.objects.get(username='wangjuan').user_permissions.values()
    #Permission.objects.create(content_type_id=10,codename='codename',name='wangjuan')
    ## delete permission called codename, which can find in the mysqldb in table auth_permissions
    #Permission.objects.get(codename='codename').delete()
    #print 'wangjuans all perms -------',User.objects.get(username='wangjuan').user_permissions.values()

    ##create users
    ## jack = User.objects.create_user('jack', 'jack@example.com', 'topsecretagentjack')
    ## admins = Group.objects.create(name='admins')
    ## print jack.has_perm('change_group', admins)
    #username.user_permissions.all()
    #Group.objects.get(user=current_user_set)
    return render_to_response('user_list.html', {'user_all': user_all,'group_all': group_all,'session_role_id':session_role_id})



def user_edit(request):
    header_title, path1, path2 = '编辑用户', '用户管理', '编辑用户'
    if request.method == 'GET':
        user_id = request.GET.get('id')
        #print '-----------------', user_id
        if not user_id:
            #return HttpResponseRedirect(reverse('index'))
            return HttpResponseRedirect('/userlist/')

        user_role = {'SU': u'超级管理员', 'CU': u'普通用户'}
        user = User.objects.get( id=user_id)
        #print user
        #username = User.objects.get( id = user_id )
        group_all = Group.objects.all()
        #print group_all
        if user:
            #groups_str = ' '.join([str(group.id) for group in user.group.all()])
            #admin_groups_str = ' '.join([str(admin_group.group.id) for admin_group in user.admingroup_set.all()])
            return render_to_response('user_edit.html',{'user':user,'group_all':group_all})

    else:
        #print '-------reurl to post------'
        user_id = request.GET.get('id')
        #print '-----user id-------',user_id
        password = request.POST.get('password')
        name = request.POST.get('name')
        email = request.POST.get('email')
        groups = request.POST.getlist('groups')
        #print '--------selected group------',groups[0]
        group_id = int(groups[0])
        group_name = Group.objects.all()
        #print '--------groups-------',group_name[group_id]

        role_post = request.POST.get('role', 'CU')
        admin_groups = request.POST.getlist('admin_groups', [])
        #print '----------all groups----',admin_groups
        extra = request.POST.getlist('extra', [])
        is_active = True if '0' in extra else False
        email_need = True if '1' in extra else False
        user_role = {'SU': u'超级管理员', 'GA': u'部门管理员', 'CU': u'普通用户'}

        if user_id:
            user = User.objects.get(id=user_id)
            
            #print '------username---',user
        else:
            return HttpResponseRedirect(reverse('/user_list/'))

        ##db_update_user(user_id=user_id,
        ##               password=password,
        ##               username=name,
        ##               email=email,
        ##               groups=groups,
        ##               admin_groups=admin_groups,
        ###               role=role_post,
        ##               is_active=is_active)
        #print user.has_perm('change_group')

        ## test if a user have some perm, if have, return true, if not, return false
        #user1 = User.objects.get(id=49)
        #print user1.has_perm('change_group')


        ##modify users information without creating a new one
        user.last_name = name
        user.password = make_password(password,None,'pbkdf2_sha256')
        #print '-----------encrypted password-------',user.password
        user.email = email
        username = request.POST.get('username')
        #print '---------username------',username
        email = request.POST.get('email')
        user.last_name = username
        user.save()

        if email_need:
            msg = u"""
            Hi %s:
                您的信息已修改，请登录运维系统查看详细信息
                地址：%s
                用户名： %s
                密码：%s (如果密码为None代表密码为原密码)
                权限：：%s
            """ % (user.name, URL, user.username, password, user_role.get(role_post, u''))
            send_mail('您的信息已修改', msg, MAIL_FROM, [email], fail_silently=False)

        #return HttpResponseRedirect(reverse('user_list'))
        return HttpResponseRedirect('/userlist/')
    #return my_render('user_edit.html', locals(), request)
    return render_to_response('user_edit.html', request)


@permission_required('mycmd.delete_userdellist')
@login_required(login_url="/login/")
def user_del(request):
    #assign perms to user
    
    user_id = request.session.items()[1][1]
    print user_id
    username = User.objects.get( id = user_id )
    superuser = User.objects.get( id = 1 )

   
    if request.method == "GET":
    #    print 'get method'
        user_del_id = request.GET.get('id')
        user_del_id_list = user_id.split(',')

    elif request.method == "POST":
    #    print 'post method'
        user_del_id = request.POST.get('id')
        user_del_id_list = user_id.split(',')
    else:
    #    print 'error'
        return HttpResponse('错误请求')

    #print 'user id',user_id
    #print 'user id list',user_id_list
    #del_object = UserDelList.objects.create(deleted_user_id_id=user_id,deleted_by=username,delete_result='success')
    #assign_perm('mycmd.delete_userdellist',username)
    
    user_del_username = User.objects.get( id = user_del_id )
    print 'user_del_username',user_del_username

    '''conf = ConfigParser.SafeConfigParser()
    conf.read('/usr/local/src/cmdb/saltcmd/mycmd/ldap.conf')
    ldap_server = conf.get("ldap","server")
    ldap_admin_user = conf.get("ldap", "admin_user")
    ldap_pass = conf.get("ldap", "pass")
    ldap_dn = conf.get("ldap", "dn")

    #connect to servers
    server = Server(ldap_server)
    conn = Connection(server,ldap_admin_user, ldap_pass, auto_bind=True)
    #conn.bind()

    user_dn = 'uid=' + str(user_del_username) + ',' + 'ou=People,ou=privileges,' + str(ldap_dn)
    print user_dn

    conn.bind()
    conn.delete(user_dn)
    #conn.delete(user_dn)  ##comparing with add operation, delete just need dn to delete a user
    conn.unbind()'''

    del_object = UserDelList.objects.create(deleted_user_id_id=user_del_id,deleted_by=username,delete_result='success')
    del_object.del_user_task()
    

    #user = User.objects.get(id=user_id)
    #print user
    #if user.last_name != 'root' and user.username != 'root':
    #    user.delete()

    return HttpResponse('删除成功')


@login_required(login_url="/login/")
def perms_add(request):
    session_role_id = 2
    if request.method == 'GET':
        print 'request method is get-------'
        #form = LoginForm()
        form = Permission()
        user_all = User.objects.all()
        group_all = Group.objects.all()
        print '---all groups----',group_all
        perm_all = Permission.objects.all()
        print '---all perms----',perm_all
        relist = {'re':'initialisze successfully'}
        #return JsonResponse(relist)
        #return render_to_response('perms_manage.html',{'group_all':group_all,'perm_all':perm_all},context_instance=RequestContext(request))
        return render_to_response('perms_manage.html',{'group_all':user_all,'perm_all':perm_all},context_instance=RequestContext(request))

    else:
        user_all = User.objects.all()
        group_all = Group.objects.all()
        perm_all = Permission.objects.all()

        group = request.POST.get('groups')
        user = request.POST.get('groups')
        print '----------------1------------------',group
        #groupname = Group.objects.get(id =group)
        username = User.objects.get(id =user)
        #print '----------------2------------------',groupname
        codename = request.POST.getlist('permall')
        print '----------------3------------------',codename
        #print '----------------4------------------',groupname.permissions.all()

        for perm in codename:
            permname = Permission.objects.filter(id = perm)
            print '----------------6------------------',permname
            ##if the permname in the groups perm, then you can return a note that you already have a perm about this
            #if permname[0] in groupname.permissions.all():
            if permname[0] in username.user_permissions.all():
                ## relist = {'re':'this perm already exist, please choose again'}
                ## #return render_to_response('perms_manage.html',context_instance=RequestContext(request))
                ## return JsonResponse(relist)
                print '-----------------7----------------'
            ##if the permname not in the groupname perms, then you can add a new perm in the group
            else:
                #Permission.objects.create(content_type_id=int(content_type_id),codename=codename,name=name)
                ## groupname.permissions.add(codename)
                ## relist = {'re':'add perms successfully'}
                ## #return JsonResponse(relist)
                ## return render_to_response('perms_manage.html',context_instance=RequestContext(request))
                print '-----------------add new perm to the group----------------'
                #groupname.permissions.add(perm)
                username.user_permissions.add(perm)
                #assign_perm('mycmd.change_userdellist',username) ##user assign can meet the demand


        #return render_to_response('perms_manage.html',{'group_all':group_all,'perm_all':perm_all},context_instance=RequestContext(request))
        return render_to_response('perms_manage.html',{'group_all':user_all,'perm_all':perm_all},context_instance=RequestContext(request))

@permission_required('mycmd.delete_userdellist')
@login_required(login_url="/login/")    
def perms_delete(request):
    codename = request.POST['codename']
    Permission.objects.get(codename=codename).delete()
    relist = {'re':"该权限删除成功!"}
    return render_to_response('perms_manage.html',request)

@permission_required('mycmd.delete_userdellist')
@login_required(login_url="/login/")
def update_list(request):
    jids = []
    to_be_updated_data = UpdateFilesDB.objects.filter(update_outcome='progressing')
    #jids = [row[0] for row in to_be_updated_data]
    for jid in to_be_updated_data:
        jids.append(jid)
        print type(jid)
    print jids
    for each_jid in jids:
        succeeded_gmsv = []
        succeeded_gmsv_detail = []
        failed_gmsv = []
        failed_gmsv_detail = []
        failed_gmsv_id = []
        succeeded_gmsv_id = []

        opts = salt.config.master_config('/etc/salt/master')
        runner = salt.runner.RunnerClient(opts)
        outcome = runner.cmd('jobs.lookup_jid', [str(each_jid)])

        '''所有服务器数量count'''
        ret=[]
        client = salt.client.LocalClient()
        minions = client.cmd('*', 'test.ping')
        #print ret['up'],type(ret['up'])
        print minions,type(minions),len(minions)

        '''如果存活的服务器和监测到的jid返回结果一致，也就是说salt异步执行已经完全执行完毕，就可以进行更新了，如果没有更新完毕，则返回之前的结果'''
        if len(outcome) == len(minions):
            print '-----------outcome------',outcome
            for key in outcome:
                print '-----key----',key
                count = len(outcome[key])
                for i in range(count):
                    print outcome
                    print '--------------',outcome[key][i]['runstatus'],type(outcome[key][i]['runstatus'])
                    if outcome[key][i]['runstatus'] == 0:
                        succeeded_gmsv_id.append(outcome[key][i]['gameserver'])
                        succeeded_gmsv_item = {'gmsvid':outcome[key][i]['gameserver'],'status':outcome[key][i]['runstatus'],'details':outcome[key][i]['details']}
                        print '------------sunccess item---------',succeeded_gmsv_item
                        succeeded_gmsv_detail.append(succeeded_gmsv_item)
                    else:
                        failed_gmsv_id.append(outcome[key][i]['gameserver'])
                        failed_gmsv_item = {'gmsvid':outcome[key][i]['gameserver'],'status':outcome[key][i]['runstatus'],'details':outcome[key][i]['details']}
                        print '------------sunccess item---------',failed_gmsv_item
                        failed_gmsv_detail.append(failed_gmsv_item)
    
                '''判断操作是否成功'''
            if failed_gmsv_id:
                update_status = 'Fail'
            else:
                update_status = 'Success'
            '''每个jid更新后的结果存入数据库'''
            item = UpdateFilesDB.objects.get(result_jid=each_jid)
            item.update_outcome = update_status
            item.update_fail_server = failed_gmsv_id
            item.update_fail_details = failed_gmsv_detail + succeeded_gmsv_id
            item.save()
        else:
            pass

    update_log = UpdateFilesDB.objects.order_by('-update_time')[:10]
    perm_all = Permission.objects.all()
    return render_to_response('list.html', {'outcomes':update_log,'perm_all':perm_all},context_instance=RequestContext(request))

@permission_required('mycmd.delete_userdellist')
@login_required(login_url="/login/")
def update_progress(request):
    if request.method == 'POST':
        '''update_jid=request.POST.get('result_jid')
        user_input = UpdateFilesDB.objects.get(jid=update_jid)
        is_all_gameservers = UpdateFilesDB.objects.filter(update_jid).value('is_all_gameservers')
        print is_all_gameservers,type(is_all_gameservers)
        input_gameserver_id = UpdateFilesDB.objects.filter(update_jid).value('input_gameserver_id')
        print input_gameserver_id,len(input_gameserver_id)
        exclu_gameserver_id = UpdateFilesDB.objects.filter(update_jid).value('exclu_gameserver_id')
        print exclu_gameserver_id,len(exclu_gameserver_id)
        if is_all_gameservers == 'Yes':
            exclu_account = len(exclu_gameserver_id)
            allgmsv = GamesvList.objects.all().count() - exclu_gameserver_id
        else:
            input_account = len(input_gameserver_id)
            allgmsv = input_account

        
        opts = salt.config.master_config('/etc/salt/master')
        runner = salt.runner.RunnerClient(opts)
        outcome = runner.cmd('jobs.lookup_jid', [str(update_jid)])
        finishedgmsv = 0
        for key in outcome:
            finishedgmsv = finishedgmsv + len(outcome[key])
        #print '--------------finishedgmsv------',finishedgmsv
        #allgmsv = GamesvList.objects.all().count()
        #print '--------------allgmsv------',allgmsv'''
        allgmsv = GamesvList.objects.all().count()
    else:
        update_jid = request.GET.get('result_jid')
        print UpdateFilesDB.objects.get(result_jid = update_jid).is_all_gameservers,type(UpdateFilesDB.objects.get(result_jid = update_jid).is_all_gameservers)
        #print is_all_gameservers,type(is_all_gameservers)
        print UpdateFilesDB.objects.get(result_jid = update_jid).input_gameserver_id,type(UpdateFilesDB.objects.get(result_jid = update_jid).input_gameserver_id)
        #print input_gameserver_id,len(input_gameserver_id)
        print UpdateFilesDB.objects.get(result_jid = update_jid).exclu_gameserver_id,type(UpdateFilesDB.objects.get(result_jid = update_jid).exclu_gameserver_id)
        #print exclu_gameserver_id,len(exclu_gameserver_id)


        print update_jid
        opts = salt.config.master_config('/etc/salt/master')
        runner = salt.runner.RunnerClient(opts)
        outcome = runner.cmd('jobs.lookup_jid', [str(update_jid)])
        finishedgmsv = 0
        for key in outcome:
            finishedgmsv = finishedgmsv + len(outcome[key])
        #print '--------------finishedgmsv------',finishedgmsv
        allgmsv = GamesvList.objects.all().count()
        print '--------------allgmsv------',allgmsv

    #time.sleep(5)
    perm_all = Permission.objects.all()
    '''暂时将文件的返回值修改成为全部成功，后面做完采集所有的服务器信息后再完善这里的进度,这个地方需要讨论很多情况,后续会画出逻辑图'''
    #ret = {"finishedgmsv":finishedgmsv,"allgmsv":allgmsv,"result_jid":update_jid}
    ret = {"finishedgmsv":allgmsv,"allgmsv":allgmsv,"result_jid":update_jid}
    print ret
    ## dump data to html, this data need to be json format
    ret_json = json.dumps(ret)
    '''return {'finishedgmsv':finishedgmsv,'allgmsv':allgmsv}'''
    return HttpResponse(ret_json)

@permission_required('mycmd.delete_userdellist')
@login_required(login_url="/login/")
def big_file_download(request):
    run_jid=request['update_jid']
    opts = salt.config.master_config('/etc/salt/master')
    runner = salt.runner.RunnerClient(opts)
    logfilename = '/var/log/' + run_jid + '.log'
    outcome = runner.cmd('jobs.lookup_jid', [str(update_jid)])
    f = open(logfilename,'w')
    f.write(outcome)
    f.close
    content = open("simplefile", "rb").read()
    return HttpResponse(content)

@permission_required('mycmd.delete_userdellist')
@login_required(login_url="/login/")
def file_download(request):
    if request.method == 'POST':
        run_jid=request['update_jid']
        opts = salt.config.master_config('/etc/salt/master')
        runner = salt.runner.RunnerClient(opts)
        logfilename = '/var/log/' + run_jid + '.log'
        if request.POST.has_key('s_thread'):
            #filename = '/root/dist.tar.gz'
            wrapper = FileWrapper(file(logfilename))
            response = HttpResponse(wrapper, content_type='text/plain')
            response['Content-Length'] = os.path.getsize(logfilename)
            response['Content-Encoding'] = 'utf-8'
            response['Content-Disposition'] = 'attachment;filename=%s' % filename
            return response
    return render(request,'list.html',locals())

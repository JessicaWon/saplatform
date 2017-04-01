import ConfigParser
from ldap3 import Server, Connection, SUBTREE
from ldap3 import HASHED_SALTED_SHA256
from ldap3.utils.hashed import hashed
from passlib.hash import ldap_md5_crypt as md5encode
from django.template import RequestContext

import crypt
class ldap_manage:
    conf = ConfigParser.SafeConfigParser()
    conf.read('/usr/local/src/cmdb/saltcmd/mycmd/ldap.conf')
    ldap_server = conf.get("ldap","server")
    ldap_admin_user = conf.get("ldap", "admin_user")
    ldap_pass = conf.get("ldap", "pass")
    ldap_dn = conf.get("ldap", "dn")

    def ldap_user_add(self):
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
    def ldap_user_delete(self):
        server = Server(ldap_server)
        conn = Connection(server,ldap_admin_user, ldap_pass, auto_bind=True)
        conn.bind()

        user_dn = 'uid=' + username + ',' + 'ou=People,ou=privileges,' + ldap_dn
        print user_dn

        conn.delete(user_dn)  ##comparing with add operation, delete just need dn to delete a user
        conn.unbind()
        print 'delete user successfully'

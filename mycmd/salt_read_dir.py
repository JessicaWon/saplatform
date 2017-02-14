import os
import os.path
import json
#--------------------this script gets all the dirs and files---------------
p_id = 1
p_pid = 0
jsondict = dict()
jsonlist = list()
dirpath = r"/opt"  # p_id=1 ,p_pid =0
#jsonlist = []
#jsondict = {"id": 1, "pId": 0, "path": dirpath, "name": "tree"}
#jsonlist.append(jsondict)


def getnumlength(fnum=0):
    numlength = 0
    while(fnum > 0):
        fnum = fnum / 10
        numlength += 1
    print numlength
    return numlength


def get_id_pid(root,jsonlist):
    for x in jsonlist:
        if x["path"] == root:
            print x
            return x["id"]


def getfile(dirpath):
#    jsonlist = []
    jsonlist = []
    jsondict = {"id": 1, "pId": 0, "path": dirpath, "name": "/srv"}
    jsonlist.append(jsondict)

    list_dirs = os.walk(dirpath)
    for root, dirs, files in list_dirs:
        fnum = 1
        global p_id
        numlength = getnumlength(fnum)
        c_pid = get_id_pid(root,jsonlist)
#        jsonlist = []
        for d in dirs:
            # c_pid = p_id

            c_id = c_pid * pow(10, numlength) + fnum
            fnum += 1
            print os.path.join(root, d), c_pid, c_id, d, root
            jsondict = {"id": c_id, "pId": c_pid,
                        "path": os.path.join(root, d), "name": d}
            jsonlist.append(jsondict)
        for f in files:
            # c_pid = p_id

            c_id = c_pid * pow(10, numlength) + fnum
            fnum += 1
            print os.path.join(root, f), c_pid, c_id, f, root
            jsondict = {"id": c_id, "pId": c_pid,
                        "path": os.path.join(root, d), "name": f}

            jsonlist.append(jsondict)
    
#    jsonlist.append(jsondict)
    return jsonlist

#getfile(dirpath)
#print '###################################################################'

#print json.dumps(jsonlist)

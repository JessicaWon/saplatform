import os
import os.path
import json

dir_path = '/opt'

def get_path_treeview(dir_path):
    p_id = 1
    p_pid = 0
    jsondict = dict()
    jsonlist = list()
    jsondict = {"id": 1, "pId": 0, "path": dir_path, "name": dir_path}
    jsonlist.append(jsondict)

    c_id = 1
    c_pid = 1
    for dirname in os.listdir(dir_path):
        if os.path.isdir(dir_path+'/'+dirname):
            dir_sub_path = os.path.abspath(dir_path+'/'+dirname)
            #print(file_sub_path)
            c_id += 1
            jsondict = {"id": c_id, "pId": c_pid,"path": dir_sub_path, "name": dirname}
            jsonlist.append(jsondict)
        else:
             pass
    return jsonlist
get_path_treeview(dir_path)
abc = get_path_treeview(dir_path)
print json.dumps(abc)

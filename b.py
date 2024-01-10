import json
import subprocess
import datetime
import os

sheets_id = ""
api_key = ""

def main():
    kadai_progress = get_progress()
    user_list = get_user(kadai_progress)
    absolute_path = get_path()
    kubectl_history = get_history(user_list)
    kadai_time = get_log(user_list)
    command_list = delete_command(kadai_progress, user_list, kubectl_history, absolute_path, kadai_time)
    run_delete(command_list)

def get_user(kadai_progress):
    user_list = []
    with open("/etc/passwd", "r") as f:
        for i in f:
            if "home" in i and "/bin/bash" in i:
                u = []
                for j in i:
                    if j == ":":
                        break
                    else:
                        u.append(j)
                for user_id in kadai_progress:
                    if user_id["学籍番号"].upper() == "".join(u).upper():
                        user_list.append("".join(u))
    return user_list

def get_path():
    root_directory = "/home"
    py_files = []
    for foldername, subfolders, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.endswith(".yml"):
                py_files.append(os.path.abspath(os.path.join(foldername, filename)))
            if filename.endswith(".yaml"):
                py_files.append(os.path.abspath(os.path.join(foldername, filename)))
    return py_files

def get_history(user_list):
    kubectl_history = {}
    for user in user_list:
        with open("/home/" + user +"/.bash_history") as f:
            command_history = []
            switch = False
            for i in f:
                if i[0] == "#":
                    lis = []
                    command_time = (datetime.datetime.fromtimestamp(int(i[1:])) + datetime.timedelta(hours=9)).strftime('%F %T')
                    switch = True
                    lis.append(command_time)
                    continue
                if switch:
                    if "kubectl" in i and "apply" in i:
                        lis.append(i.replace("\n", ""))
                        command_history.append(lis)
                    switch = False
            kubectl_history[user] = command_history
    return kubectl_history
    
def get_progress():
    with open('kadai_progress.json', "w") as kadai_progress_file:
        subprocess.run(["curl", "https://sheets.googleapis.com/v4/spreadsheets/" + sheets_id + "/values/Progress?key=" + api_key], stdout=kadai_progress_file)
    with open('kadai_progress.json', "r") as kadai_progress_file:
        kadai_spreadsheet = json.load(kadai_progress_file)
    all_kadai_progress_list = kadai_spreadsheet["values"]
    group_number = ""
    all_kadai_progress_dict = []
    for i in all_kadai_progress_list:
        if i[0] == "":
            i[0] = group_number
        else:
            group_number = i[0]
        if i == all_kadai_progress_list[0]:
            continue
        else:
            dic = {}
            for j in range(len(i)):
                dic[all_kadai_progress_list[0][j]] = i[j]
            all_kadai_progress_dict.append(dic)
    vm_name = subprocess.run(["hostname"], encoding='utf-8', stdout=subprocess.PIPE).stdout.replace("\n", "")
    group_kadai_progress = []
    for i in all_kadai_progress_dict:
        if i["Group"][-3:] == vm_name[-4:-1]:
            group_kadai_progress.append(i)
    return group_kadai_progress

def get_log(user_list):
    with open('spreadsheet_log.json', "w") as spreadsheet_log_file:
        subprocess.run(["curl", "https://sheets.googleapis.com/v4/spreadsheets/" + sheets_id + "/values/Log?key=" + api_key], stdout=spreadsheet_log_file)
    with open('spreadsheet_log.json', "r") as spreadsheet_log_file:
        log_spreadsheet = json.load(spreadsheet_log_file)
    log_spreadsheet_list = log_spreadsheet["values"]
    kadai_time = {}
    for user in user_list:
        list = []
        for j in log_spreadsheet_list:
            try:
                if j[1].upper() == user.upper() and "完了" in j:
                    list.append(j)
            except:
                continue
        kadai_time[user] = list
    return kadai_time
        
def delete_command(kadai_progress, user_list, kubectl_history, absolute_path, kadai_time):
    command_list = []
    for user in user_list:
        for kadai in kadai_time[user]:
            for history in kubectl_history[user]:
                if history[0] < kadai[0]:
                    file = history[1].split()
                    if user.upper() in file or user.lower() in file:
                        for j in file:
                            if "." in j:
                                f = j
                                break
                        for path in absolute_path:
                            if f in path and user in path:
                                for num in range(len(file)):
                                    if "." in file[num]:
                                        file[num] = path
                                    if "apply" in file[num]:
                                        file[num] = "delete"
                        command_list.append(file)
    return command_list

def run_delete(command_list):
    for command in command_list:
        subprocess.run(command)

if __name__ == "__main__":
    main()
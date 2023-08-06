import typer
import socket
import json
import pyperclip
import time as timer
from time import time
import os
from tabulate import tabulate
import wcwidth
import urllib3
from uuid import getnode as get_mac
import sys
from pathlib import Path
import subprocess
import re

downloads_path = str(Path.home() / "Downloads")

HOST = "localhost"
PC_PORT = 19091
FIRST_TASK_TAG = 'Zmlyc3QgdGFzaw=='

MAC_ADDRESS = '-'.join(['{:02X}'.format((get_mac() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])
URL = "https://cloudapi.bytedance.net/faas/services/ttpduz/invoke/caoEvent"

app = typer.Typer()


def start():
    print("Hello")


FILE_PATH = 'cache.json'


def put(task):
    if len(task['method']['params']) == 0:
        return
    with open(FILE_PATH, 'w+') as file:
        data = {}
        try:
            data = json.load(file)
        except ValueError as e:
            sys.stderr.write("e")
        if str(task['key']) in data:
            old_list = data[task['key']]
        else:
            old_list = []
        for idx, item in enumerate(old_list):
            if item == task:
                old_list.insert(0, old_list.pop(idx))
                return
        old_list.insert(0, task)
        data[task['key']] = old_list
        json.dump(data, file)


def get(key):
    with open(FILE_PATH, 'r+') as file:
        data = json.load(file)
        return data[key]


def has_key(key):
    with open(FILE_PATH, 'r+') as file:
        data = json.load(file)
        return str(key) in data


def clear():
    with open(FILE_PATH, 'w+') as file:
        json.dump({}, file)


def create_file_if_not_exists():
    cache_file = Path(FILE_PATH)
    cache_file.touch(exist_ok=True)
    file = open(FILE_PATH, "w+")
    data = file.read()
    if not data:
        file.write("{}")


@app.command(name="list")
def list(search: str = typer.Argument("")):
    try:
        create_file_if_not_exists()
        start_time = current_milli_time()
        os.system('source ~/.bash_profile &')
        # 这里暂存到临时文件中，避免控制台输出
        os.system('adb forward tcp:19091 tcp:19191 > temp.log')

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PC_PORT))
        sock.send("\n".encode())
        response = get_all_data(sock)
        sock.close()
        tasks = json.loads(response.decode('utf-8'))
        mobLoadTasks(current_milli_time() - start_time)
        print_list = []
        search_list = []
        for index, task in enumerate(tasks, 1):
            if re.search(search, str(task['title']), re.IGNORECASE) or re.search(search, str(task['key']), re.IGNORECASE):
                search_list.append(task)
                print_item = [len(search_list), task['title'], task['ownerName'], task['emailPrefix'], task['key']]
                print_list.append(print_item)

        execute_start = current_milli_time()
        if len(search_list) == 1:
            execute_task(execute_start, search_list[0])
        elif len(search_list) == 0:
            typer.secho("请检查任务过滤关键词")
        else:
            typer.secho(tabulate(print_list, headers=["ID", "TITLE", "AUTHOR", "Email", "Key"], tablefmt='pretty'),
                        fg=typer.colors.BLUE, bold=True)
            typer.secho("\n")

            task_id = typer.prompt("需要执行哪个任务? (输入ID)")
            task = search_list[int(task_id) - 1]

            execute_task(execute_start, task)
    except Exception:
        typer.secho("\n")
        typer.secho("执行异常，可能的原因如下：", err=True)
        typer.secho("\t 1. 未启动测试包", err=True)
        typer.secho("\t 2. 未通过USB连接手机", err=True)
        typer.secho("\t 3. 中断任务执行", err=True)


def execute_task(execute_start, task):
    if has_key(task['key']):
        cache_list = []
        input_item = [1, "重新输出参数"]
        cache_list.append(input_item)
        for cache_idx, cache in enumerate(get(task['key']), 2):
            cache_item = [cache_idx, ','.join(cache['method']['params'])]
            cache_list.append(cache_item)
        typer.secho(tabulate(cache_list, headers=["ID", "Parameters"], tablefmt='pretty'), fg=typer.colors.BLUE,
                    bold=True)
        typer.secho("\n")

        cache_id = typer.prompt("选择缓存项")

        if cache_id == '1':
            input_params(task)
        else:
            task = get(task['key'])[int(cache_id) - 2]
    else:
        input_params(task)
    rsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rsock.connect((HOST, PC_PORT))
    rsock.send(FIRST_TASK_TAG.encode())
    rsock.send("\n".encode())
    rsock.send(json.dumps(task).encode())
    rsock.send("\n".encode())
    response = get_all_data(rsock)
    rsock.close()
    put(task)
    mobExecuteMethodEvent(task['key'], current_milli_time() - execute_start)
    if task['outputType'] == 0:
        pyperclip.copy(response.decode("utf-8"))
        typer.secho(str(response.decode('utf-8')), fg=typer.colors.BLUE, bold=True)
    elif task['outputType'] == 2:
        time_str = timer.strftime("%Y-%m-%d-%H_%M_%S")
        file_name = downloads_path + time_str + ".json"

        typer.secho("Output file path: " + file_name)

        try:
            f = open(file_name, 'w')
            f.write(json.dumps(json.loads(response)))
            f.close()

            os.system("open " + file_name)
        except Exception:
            typer.secho("JSON 格式异常，请检查输出是否为JSON文件", err=True)
    else:
        # 列表结果
        list_tasks = json.loads(response.decode('utf-8'))

        print_list = []
        for index, task in enumerate(list_tasks, 1):
            print_item = [index, task['title'], task['subTitle']]
            print_list.append(print_item)
        typer.secho(tabulate(print_list, headers=["ID", "TITLE", "SUBTITLE"], tablefmt='simple'),
                    fg=typer.colors.BLUE, bold=True)
        typer.secho("\n")

        selected_index = typer.prompt("选择其中一个选项(输入ID)")
        selected_task = list_tasks[int(selected_index) - 1]

        print_list = []
        for index, task in enumerate(selected_task['options'], 1):
            print_item = [index, task['title'], task['subTitle']]
            print_list.append(print_item)
        typer.secho(tabulate(print_list, headers=["ID", "TITLE", "SUBTITLE"], tablefmt='simple'),
                    fg=typer.colors.BLUE, bold=True)
        typer.secho("\n")

        option_index = int(typer.prompt("选择操作项(输入ID)")) - 1
        selected_start_time = current_milli_time()
        executed_method(json.dumps(selected_task['options'][option_index]))
        mobExecuteMethodEvent(selected_task['key'], current_milli_time() - selected_start_time)


def input_params(task):
    params_hint = task['method']['paramsHint']
    # Input Params
    for index, paramHint in enumerate(params_hint, 0):
        task['method']['params'].append(typer.prompt(task['method']['paramsHint'][index]))


def executed_method(task_str):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PC_PORT))
    sock.send(FIRST_TASK_TAG.encode())
    sock.send("\n".encode())
    sock.send(task_str.encode())
    sock.send("\n".encode())
    response = get_all_data(sock)
    sock.close()
    typer.secho(response, fg=typer.colors.GREEN, bold=True)


def get_all_data(sock):
    BUFF_SIZE = 4096  # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data


def current_milli_time():
    return int(time() * 1000)


def exec_command(cmd):
    return subprocess.getoutput(cmd)


def get_git_name():
    return exec_command("git config user.name")


def get_git_email():
    return exec_command("git config user.email")


def get_name():
    email = get_git_email()
    name = get_git_name()
    if email:
        return email
    else:
        return name


def mobExecuteMethodEvent(key, duration):
    http = urllib3.PoolManager()
    PARAMS = {"event": "execute_method",
              "key": key,
              "id": MAC_ADDRESS,
              "client": "CLI",
              "name": get_name(),
              "duration": duration,
              "time_stamp": current_milli_time()
              }
    http.request('GET', URL, fields=PARAMS)


def mobLoadTasks(duration):
    http = urllib3.PoolManager()
    PARAMS = {"event": "load_tasks", "client": "CLI", "id": MAC_ADDRESS, "duration": duration,
              "name": get_name(),
              "time_stamp": current_milli_time()}
    http.request('GET', URL, fields=PARAMS)

from flask import Flask, Response
from datetime import datetime, timedelta, time
import os
import subprocess
import json
import re

app = Flask(__name__)

@app.route('/')
def hello_world():
    serverstatus = {}
    serverstatus['disks'] = get_disk_space()
    serverstatus['memory'] = get_memory()
    serverstatus['cpu'] = get_cpu()
    serverstatus['power'] = get_power()
    lastmodified = datetime.now() - timedelta(minutes=1)
    headers = {'Last-Modified': lastmodified.ctime()}
    headers = {'Etag': datetime.now().ctime()}
    return Response(response=json.dumps(serverstatus), status=200, mimetype='application/json', headers=headers)
    #return str(", ".join(disks[1]))

def get_disk_space():
    disks = ['/media/1tb', '/media/terry', '/media/320gb']
    result = {}
    for disk in disks:
        df = subprocess.Popen(["df", "-h", disk], stdout=subprocess.PIPE)
        output = df.communicate()[0]
        device, size, used, available, percent, mountpoint = \
            output.split("\n")[1].split()
        # result.append(output.split("\n")[1])
        result[disk] = {
            'name': disk,
            'device': device,
            'size': size,
            'used': used,
            'available': available,
            'percent': percent,
            'mountpoint': mountpoint}
    return result

def get_memory():
    memory = {}
    free = subprocess.Popen(["free"], stdout=subprocess.PIPE)
    output = free.communicate()[0]
    type, total, used, free, shared, buffers, cached = \
        output.split("\n")[1].split()
    memory['ram'] = {
            'type': type[:-1],
            'total': byte_to_human(total),
            'used': byte_to_human(int(used) - int(cached)),
            'free': byte_to_human(free),
            'shared': byte_to_human(shared),
            'buffers': byte_to_human(buffers),
            'cached': byte_to_human(cached)}
    type, total, used, free = \
        output.split("\n")[3].split()
    memory['swap'] = {
            'type': type[:-1],
            'total': byte_to_human(total),
            'used': byte_to_human(used),
            'free': byte_to_human(free),
            }
    return memory


def get_cpu():
    uptime = subprocess.Popen(["uptime"], stdout=subprocess.PIPE)
    output = uptime.communicate()[0]
    onemin, fivemin, fifteenmin = output.strip().split()[-3:]
    servertime, dumb, users = output.split(", ")[:3]
    return {
        "load": {
            1: onemin[:-1], 
            5: fivemin[:-1], 
            15: fifteenmin,
            "string": output.split(":")[4].strip()},
        "servertime": datetime.now().strftime("%a %I:%M %P"),
        "users": users.strip(),
        "uptime": " ".join(servertime.split()[-2:]),
        "temperature": get_cpu_temp()
        }
    #return output.split("\n")[0].split()[-3:]

def get_cpu_temp():
    uptime = subprocess.Popen(["cat", "/proc/acpi/thermal_zone/TZ01/temperature"], stdout=subprocess.PIPE)
    output = uptime.communicate()[0]
    cur_temp = output.strip().split()[1]

    uptime = subprocess.Popen(["cat", "/proc/acpi/thermal_zone/TZ01/trip_points"], stdout=subprocess.PIPE)
    output = uptime.communicate()[0]
    max_temp = output.strip().split("\n")[0].split()[2]
    return {"current_temp": cur_temp + "C", "critical_temp": max_temp + "C"}

def byte_to_human(kb):
    mb = float(kb) / 1024
    gb = mb / 1024
    if gb > 1:
        return format(gb, '.1f') + "g"
    elif mb > 1:
        return format(mb, '.1f') + "m"
    else:
        return str(kb) + "k"

def get_power():
    pwrstatus = subprocess.Popen(["pwrstat", "-status"], stdout=subprocess.PIPE)
    output = pwrstatus.communicate()[0]
    power = {}
    for l in output.split("\n"):
        if len(l) > 0 and l.count(".") > 1:
            l = re.sub(r'\.+', '\t', l.strip())
            parts = l.split("\t")
            power[parts[0]] = parts[1].strip()
    return power

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')


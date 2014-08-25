from simplejson import dumps as json_dumps

from flask import Flask, Response
from flask.templating import render_template

from api_call import get_data_from_api
from system_apis.hardware import *

from config import *
from constants import *

app = Flask(__name__)


@app.route('/')
def home():

    cpu_info = get_data_from_api(API_URL.format(CPU_URL))
    ram_info = get_data_from_api(API_URL.format(RAM_URL))
    network = get_data_from_api(API_URL.format(NETWORK_USAGE_URL))
    processes = get_data_from_api(API_URL.format(PROCESS_URL + ','.join(PROCESSES)))

    disks_data = {}
    for disk in DISKS:
        data = get_data_from_api(API_URL.format(DISKS_URL + disk[1:]))
        if data:
            disks_data[disk] = data

    uptime_response = get_data_from_api(API_URL.format(UPTIME_URL))
    if uptime_response:
        uptime = uptime_response.get('uptime')
    else:
        uptime = None

    ctx = {
        'cpu': cpu_info,
        'ram': ram_info,
        'uptime': uptime,
        'network': network,
        'disks': disks_data,
        'processes': processes,

    }

    return render_template('home/home.html', ctx=ctx)


# API URLs
@app.route('/api/test', methods=['GET'])
def api_test():

    ctx = {
        'cpu_usage': get_current_cpu_usage(),
        'cpu_cores': get_cpu_cores_details(),
        'ram_total': get_ram_total_capacity(),
        'ram_usage': get_current_ram_usage(),
        'disk': get_disk_usage(),
        'network': get_network_usage(),
        'uptime': get_system_uptime(),
        'monitored_processes': get_monitored_process_states(process_list=[
            'ServerMonitorClient.py'
        ]),
    }

    return Response(response=json_dumps(ctx), mimetype="application/json")


@app.route('/api/cpu/')
def api_get_cpu_info():

    ctx = {
        'cores': get_cpu_cores_details(),
        'usage': get_current_cpu_usage(),
    }

    return Response(response=json_dumps(ctx), mimetype="application/json")


@app.route('/api/cpu/usage/')
def api_get_cpu_usage():

    ctx = {
        'cpu_usage': get_current_cpu_usage(),
    }

    return Response(response=json_dumps(ctx), mimetype="application/json")


@app.route('/api/ram/')
def api_get_ram_info():

    ctx = {
        'capacity': get_ram_total_capacity(),
        'usage': get_current_ram_usage(),
    }

    return Response(response=json_dumps(ctx), mimetype="application/json")


@app.route('/api/ram/usage/')
def api_get_ram_usage():

    ctx = {
        'ram_usage': get_current_ram_usage(),
    }

    return Response(response=json_dumps(ctx), mimetype="application/json")


@app.route('/api/uptime/')
def api_get_uptime():

    ctx = {
        'uptime': get_system_uptime()
    }

    return Response(response=json_dumps(ctx), mimetype="application/json")


@app.route('/api/network/')
def api_get_network_info():

    ctx = get_network_usage()

    return Response(response=json_dumps(ctx), mimetype="application/json")


@app.route('/api/disk/', defaults={'disk': '/'})
@app.route('/api/disk/<path:disk>')
def api_get_disk_info(disk='/'):

    if disk[:1] != '/':
        disk = '/' + disk

    ctx = get_disk_usage(mount_point=disk)

    return Response(response=json_dumps(ctx), mimetype="application/json")


@app.route('/api/process/<process_filter>')
def api_get_filtered_processes(process_filter=None):
    ctx = []
    if process_filter:
        process_filter = process_filter.split(',')
        ctx = get_monitored_process_states(process_list=process_filter)

    return Response(response=json_dumps(ctx), mimetype="application/json")


if __name__ == '__main__':
    app.config.from_pyfile("config.py")
    app.run(threaded=True, host='0.0.0.0')

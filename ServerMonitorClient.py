from simplejson import dumps as json_dumps

from flask import Flask, Response
from flask.templating import render_template

from system_apis import api

import config

app = Flask(__name__)

DISKS = ()
PROCESSES = ()


@app.route('/')
def home():

    cpu_info = api.get_cpu_info()
    ram_info = api.get_ram_info()
    network = api.get_network_info()

    if PROCESSES:
        processes = api.get_filtered_processes(PROCESSES.split(','))
    else:
        processes = []

    disks_data = {}
    for disk in DISKS:
        data = api.get_disk_info(disk)
        if data:
            disks_data[disk] = data

    uptime_response = api.get_uptime()
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
@app.route('/api/cpu/')
def api_get_cpu_info():

    ctx = api.get_cpu_info()

    return Response(response=json_dumps(ctx), mimetype="application/json")


@app.route('/api/cpu/usage/')
def api_get_cpu_usage():

    ctx = api.get_cpu_usage()

    return Response(response=json_dumps(ctx), mimetype="application/json")


@app.route('/api/ram/')
def api_get_ram_info():

    ctx = api.get_ram_info()

    return Response(response=json_dumps(ctx), mimetype="application/json")


@app.route('/api/ram/usage/')
def api_get_ram_usage():

    ctx = api.get_ram_usage()

    return Response(response=json_dumps(ctx), mimetype="application/json")


@app.route('/api/uptime/')
def api_get_uptime():

    ctx = api.get_uptime()

    return Response(response=json_dumps(ctx), mimetype="application/json")


@app.route('/api/network/')
def api_get_network_info():

    ctx = api.get_network_info()

    return Response(response=json_dumps(ctx), mimetype="application/json")


@app.route('/api/disks/')
def api_get_all_disks_info():
    disks_data = {}
    for disk in DISKS:
        data = api.get_disk_info(disk)
        if data:
            disks_data[disk] = data

    return Response(response=json_dumps(disks_data), mimetype="application/json")

@app.route('/api/disk/', defaults={'disk': '/'})
@app.route('/api/disk/<path:disk>')
def api_get_disk_info(disk='/'):

    if not disk.startswith('/'):
        disk = '/' + disk

    ctx = api.get_disk_info(disk=disk)

    return Response(response=json_dumps(ctx), mimetype="application/json")


@app.route('/api/process/', defaults={'process_filter': PROCESSES})
@app.route('/api/process/<process_filter>')
def api_get_filtered_processes(process_filter=None):

    if not process_filter:
        process_filter = PROCESSES if PROCESSES else ''

    process_filter = process_filter.split(',')

    ctx = api.get_filtered_processes(process_filter)

    return Response(response=json_dumps(ctx), mimetype="application/json")


if __name__ == '__main__':
    config.check_config_file()
    app_config = config.load_config_file()
    PROCESSES = app_config.get('processes')
    DISKS = app_config.get('disks', '').split(',')
    app.run(threaded=True, host='0.0.0.0', debug=True)

from flask import Flask
from flask.templating import render_template
from api_call import get_data_from_api

from config import *

app = Flask(__name__)


@app.route('/', defaults={'style': 'bootstrap'})
@app.route('/<style>')
def home(style='bootstrap'):

    cpu_info = get_data_from_api(API_URL.format(CPU_URL))
    ram_info = get_data_from_api(API_URL.format(RAM_URL))
    uptime = get_data_from_api(API_URL.format(UPTIME_URL)).get('uptime')
    network = get_data_from_api(API_URL.format(NETWORK_USAGE_URL))
    processes = get_data_from_api(API_URL.format(PROCESS_URL + ','.join(PROCESSES)))

    disks_data = {}
    for disk in DISKS:
        data = get_data_from_api(API_URL.format(DISKS_URL + disk[1:]))
        if data:
            disks_data[disk] = data

    ctx = {
        'cpu': cpu_info,
        'ram': ram_info,
        'uptime': uptime,
        'network': network,
        'disks': disks_data,
        'processes': processes,

    }

    if style == 'bootstrap':
        return render_template('home/home_b.html', ctx=ctx)
    else:
        return render_template('home/home_p.html', ctx=ctx)


if __name__ == '__main__':
    app.config.from_pyfile("config.py")
    app.run(host='0.0.0.0', port=5005)

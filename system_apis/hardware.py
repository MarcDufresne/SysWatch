from datetime import datetime

import psutil

from system_apis.utils import sizeof_fmt, format_percent


def get_cpu_cores_details():
    return psutil.cpu_count()


def get_current_cpu_usage():
    return format_percent(psutil.cpu_percent(interval=1))


def get_ram_total_capacity():
    return sizeof_fmt(psutil.virtual_memory().total)


def get_current_ram_usage():
    return '{0}%'.format(psutil.virtual_memory().percent)


def get_disk_usage(mount_point='/'):
    disk_data = psutil.disk_usage(mount_point)
    return {
        'capacity': sizeof_fmt(disk_data.total),
        'used': sizeof_fmt(disk_data.used),
        'free': sizeof_fmt(disk_data.free),
        'percent': format_percent(disk_data.percent),
    }


def get_network_usage(interface='eth0'):
    net_data = psutil.net_io_counters(pernic=True)
    interface_data = net_data.get(interface)

    if not interface_data:
        interface_data = psutil.net_io_counters(pernic=False)

    return {
        'upload': sizeof_fmt(interface_data.bytes_sent),
        'download': sizeof_fmt(interface_data.bytes_recv),
    }


def get_system_uptime():
    boot_time = psutil.boot_time()
    delta = str(datetime.now() - datetime.fromtimestamp(boot_time))
    return delta[:delta.find('.')]


def get_all_process_states():
    processes = []
    for ps_process in psutil.process_iter():
        print ps_process.name()
        processes.append({
            'name': ps_process.name(),
            'pid': ps_process.pid,
            'cpu_usage': format_percent(ps_process.cpu_percent(interval=1)),
            'ram_usage': format_percent(round(ps_process.memory_percent(), 2)),
        })

    return processes


def get_monitored_process_states(process_list=()):
    processes = []
    if process_list:
        for ps_process in psutil.process_iter():
            if ps_process.name() in process_list:
                processes.append({
                    'name': ps_process.name(),
                    'pid': ps_process.pid,
                    'cpu_usage': format_percent(ps_process.cpu_percent(interval=1)),
                    'ram_usage': format_percent(round(ps_process.memory_percent(), 2)),
                })
            else:
                for arg in ps_process.cmdline():
                    for process in process_list:
                        if process in arg:
                            processes.append({
                                'name': arg,
                                'pid': ps_process.pid,
                                'cpu_usage': format_percent(ps_process.cpu_percent(interval=1)),
                                'ram_usage': format_percent(round(ps_process.memory_percent(), 2)),
                            })

    return processes

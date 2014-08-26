from hardware import *


def get_cpu_info():

    cpu_info = {
        'cores': get_cpu_cores_details(),
        'usage': get_current_cpu_usage(),
    }

    return cpu_info


def get_cpu_usage():

    cpu_data = {
        'cpu_usage': get_current_cpu_usage(),
    }

    return cpu_data


def get_ram_info():

    ram_info = {
        'capacity': get_ram_total_capacity(),
        'usage': get_current_ram_usage(),
    }

    return ram_info


def get_ram_usage():

    ram_data = {
        'ram_usage': get_current_ram_usage(),
    }

    return ram_data


def get_uptime():

    uptime_data = {
        'uptime': get_system_uptime()
    }

    return uptime_data


def get_network_info():

    network_data = get_network_usage()

    return network_data


def get_disk_info(disk='/'):

    disk_data = None
    try:
        disk_data = get_disk_usage(mount_point=disk)
    except OSError as e:
        print e.message

    return disk_data


def get_filtered_processes(process_filter=None, sort_key='cpu_usage'):
    process_list = []
    if process_filter:
        process_list = get_monitored_process_states(process_list=process_filter)

    process_list = sorted(process_list, reverse=True, key=lambda k: k.get(sort_key, None))

    return process_list
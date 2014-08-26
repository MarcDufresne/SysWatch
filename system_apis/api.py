from hardware import *


def get_cpu_info():

    ctx = {
        'cores': get_cpu_cores_details(),
        'usage': get_current_cpu_usage(),
    }

    return ctx


def get_cpu_usage():

    ctx = {
        'cpu_usage': get_current_cpu_usage(),
    }

    return ctx


def get_ram_info():

    ctx = {
        'capacity': get_ram_total_capacity(),
        'usage': get_current_ram_usage(),
    }

    return ctx


def get_ram_usage():

    ctx = {
        'ram_usage': get_current_ram_usage(),
    }

    return ctx


def get_uptime():

    ctx = {
        'uptime': get_system_uptime()
    }

    return ctx


def get_network_info():

    ctx = get_network_usage()

    return ctx


def get_disk_info(disk='/'):

    ctx = None
    try:
        ctx = get_disk_usage(mount_point=disk)
    except OSError as e:
        print e.message

    return ctx


def get_filtered_processes(process_filter=None):
    ctx = []
    if process_filter:
        ctx = get_monitored_process_states(process_list=process_filter)

    return ctx
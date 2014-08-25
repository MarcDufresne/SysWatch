

def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return '%3.1f%s' % (num, 'TB')


def format_percent(value):
    return '{0}%'.format(value)

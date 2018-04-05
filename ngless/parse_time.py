def identity(x):
    return x

def cpu_p(x):
    return int(x.strip('% '))
def wallclock_parse(x):
    toks = x.strip().split(':')
    if len(toks) == 3:
        hrs, mins, secs = toks
    elif len(toks) == 2:
        hrs = 0
        mins, secs = toks
    else:
        raise ValueError("Cannot parse wall clock: {}".format(x))
    return float(secs) + int(mins) * 60 + int(hrs) * 60 * 60

headers = {
        'Command being timed' : ('command', identity),
        'User time (seconds)' : ('user_time', float),
        'System time (seconds)' : ('system_time', float),
        'Percent of CPU this job got' : ('p_cpu', cpu_p),
        'Elapsed (wall clock) time (h:mm:ss or m:ss)' : ('wallclock', wallclock_parse),
        'Elapsed (wall clock) time' : ('wallclock', wallclock_parse),
        'Average shared text size (kbytes)' : ('avg_shared_text', int),
        'Average unshared data size (kbytes)' : ('avg_unshared_text', int),
        'Average stack size (kbytes)' : ('avg_stack', int),
        'Average total size (kbytes)' : ('avg_total', int),
        'Maximum resident set size (kbytes)' : ('max_rss', int),
        'Average resident set size (kbytes)' : ('avg_rss', int),
        'Major (requiring I/O) page faults' : ('major_pg_faults', int),
        'Minor (reclaiming a frame) page faults' : ('minor_pg_faults', int),
        'Voluntary context switches' : ('vol_context', int),
        'Involuntary context switches' : ('invol_context', int),
        'Swaps' : ('swaps', int),
        'File system inputs' : ('fs_input', int),
        'File system outputs' : ('fs_output', int),
        'Socket messages sent' : ('socket_sent', int),
        'Socket messages received' : ('socket_rcvd', int),
        'Signals delivered' : ('signals_delivered', int),
        'Page size (bytes)' : ('page_size', int),
        'Exit status' : ('exitcode', int),
        }
def parse(time_output):
    res = {}
    for line in time_output.splitlines():
        line = line.strip()
        if not line:
            return res
        line = line.replace(' (h:mm:ss or m:ss)', '')
        header,value = line.split(':', 1)
        if header in headers:
            name, conv = headers[header]
            res[name] = conv(value)
        else:
            raise ValueError("Cannot parse '{}'".format(line))
    return res

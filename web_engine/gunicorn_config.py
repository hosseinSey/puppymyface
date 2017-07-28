import multiprocessing

bind = ":5000"
reload = "True"
errorlog = '-'
loglevel = 'info'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
workers = multiprocessing.cpu_count() * 2 + 1
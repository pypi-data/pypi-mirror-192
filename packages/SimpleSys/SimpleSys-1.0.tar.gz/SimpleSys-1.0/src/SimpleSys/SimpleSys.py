import psutil

class cpu():
    def percent():
        return(psutil.cpu_percent(percpu=True))

    def count():
        return(psutil.cpu_count(logical=False), psutil.cpu_count())

class ram():
    def virtual():
        return(psutil.virtual_memory())

    def swap():
        return(psutil.swap_memory())

class disks():
    def partitions():
        return(psutil.disk_partitions())

    def usage():
        return(psutil.disk_usage('/'))

class pids():
    def pids():
        PidList = psutil.pids()
        processes = []
        for q in PidList:
            w = psutil.Process(q)
            processes.append(w)
        return(processes)
    
    def ids():
        return(psutil.pids())

    def lookup(ID):
        return(psutil.Process(ID))

    def get():
        psutil.test()

class other():
    def battery():
        return(psutil.sensors_battery())

    def users():
        return(psutil.users())

    def time():
        return(psutil.boot_time())

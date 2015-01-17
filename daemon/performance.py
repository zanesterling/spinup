import psutil

def get_CPU_usage():
    return psutil.cpu_percent(interval=1)

def get_RAM_usage():
    mem = psutil.virtual_memory()
    return 100 * float(mem.used) / float(mem.total)


if __name__ == "__main__":
    print get_CPU_usage()
    print get_RAM_usage()

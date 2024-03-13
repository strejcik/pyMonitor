import psutil
import platform
from datetime import datetime
import cpuinfo
import socket
import uuid
import re
import os

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def System_information():
    # System information
    systemInformationObj = {}
    uname = platform.uname()
    systemInformationObj['system'] = f"Operating System: {uname.system}"
    systemInformationObj['node_name'] = f"Node Name: {uname.node}"
    systemInformationObj['release'] = f"OS Release: {uname.release}"
    systemInformationObj['version'] = f"Version: {uname.version}"
    systemInformationObj['machine'] = f"Hardware Identifier: {uname.machine}"
    systemInformationObj['processorv1'] = f"Processor Name: {uname.processor}"
    systemInformationObj['processorv2'] =  f"Processor Name: {cpuinfo.get_cpu_info()['brand_raw']}"
    systemInformationObj['ipaddress'] = f"IP Address: {socket.gethostbyname(socket.gethostname())}"
    systemInformationObj["macaddress"] = f"Mac Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}"

    # Boot Time
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    systemInformationObj['boot_time'] = f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"


    











    # ## Network information
    # print("="*40, "Network Information", "="*40)
    # ## get all network interfaces (virtual and physical)
    # if_addrs = psutil.net_if_addrs()
    # for interface_name, interface_addresses in if_addrs.items():
    #     for address in interface_addresses:
    #         print(f"=== Interface: {interface_name} ===")
    #         if str(address.family) == 'AddressFamily.AF_INET':
    #             print(f"  IP Address: {address.address}")
    #             print(f"  Netmask: {address.netmask}")
    #             print(f"  Broadcast IP: {address.broadcast}")
    #         elif str(address.family) == 'AddressFamily.AF_PACKET':
    #             print(f"  MAC Address: {address.address}")
    #             print(f"  Netmask: {address.netmask}")
    #             print(f"  Broadcast MAC: {address.broadcast}")
    # ##get IO statistics since boot
    # net_io = psutil.net_io_counters()
    # print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
    # print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")

    return systemInformationObj

def Cpu_information():
    # CPU information
    cpuInformationObj = {}
    # number of cores
    cpuInformationObj['physical_cores'] = f"Physical Cores: {psutil.cpu_count(logical=False)}"
    cpuInformationObj['total_cores'] = f"Total Cores: {psutil.cpu_count(logical=True)}"
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    cpuInformationObj['max_frequency'] = f"Max Frequency: {cpufreq.max:.2f}Mhz"
    cpuInformationObj['min_frequency'] = f"Min Frequency: {cpufreq.min:.2f}Mhz"
    cpuInformationObj['current_frequency'] = f"Current Frequency: {cpufreq.current:.2f}Mhz"
    # CPU usage
    print("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"Core {i}: {percentage}%")
        cpuInformationObj[f"cpu_usage_core_{i}"] = f"Core {i}: {percentage}%"

    cpuInformationObj['total_cpu_usage'] = f"Total CPU Usage: {psutil.cpu_times_percent(interval=0.4, percpu=False).system}%"
    return cpuInformationObj

def Memory_information():
    # # Memory Information
    # get the memory details
    memoryInformationObj = {}
    svmem = psutil.virtual_memory()
    memoryInformationObj['total_memory'] = f"Total Memory: {get_size(svmem.total)}"
    memoryInformationObj['available_memory'] = f"Available Memory: {get_size(svmem.available)}"
    memoryInformationObj['used_memory'] = f"Used Memory: {get_size(svmem.used)}"
    memoryInformationObj['percentage_memory'] = f"Percentage Memory: {svmem.percent}%"
    return memoryInformationObj

def Swap_information():
    # # get the swap memory details (if exists)
    swapMemoryObj = {}
    swap = psutil.swap_memory()
    swapMemoryObj['total_swap'] = f"Total Swap: {get_size(swap.total)}"
    swapMemoryObj['free_swap'] = f"Free Swap: {get_size(swap.free)}"
    swapMemoryObj['used_swap'] = f"Used Swap: {get_size(swap.used)}"
    swapMemoryObj['percentage_swap'] = f"Swap Percentage: {swap.percent}%"
    return swapMemoryObj

def Disk_information():
    # # get the swap memory details (if exists)
    diskObj = {}
    # # Disk Information
    # # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        diskObj['partition_device'] = f"Partition Device: {partition.device}"
        diskObj['partition_mountpoint'] = f"Partition Mountpoint: {partition.mountpoint}"
        diskObj['partition_filesystem'] = f"Filesystem Type: {partition.fstype}"
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        diskObj['partition_totalsize'] = f"Partition Total Size: {get_size(partition_usage.total)}"
        diskObj['partition_usedsize'] = f"Partition Used Size: {get_size(partition_usage.used)}"
        diskObj['partition_freesize'] = f"Partition Free Size: {get_size(partition_usage.free)}"
        diskObj['partition_usageperc'] = f"Partition Usage Percent: {partition_usage.percent}%"
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    print(f"Total read: {get_size(disk_io.read_bytes)}")
    diskObj['partition_totalreadbytes'] = f"Total Read Bytes: {get_size(disk_io.read_bytes)}"
    diskObj['partition_totalwritebytes'] = f"Total Write Bytes: {get_size(disk_io.write_bytes)}"
    return diskObj

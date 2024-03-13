import psutil, os, time
from . import socketio, emit
from .systemInfo import System_information, Cpu_information, Memory_information, Swap_information, Disk_information
from .main import url_viewtime, wwwtime

processlist = list()

@socketio.on('my event')
def handle_message(data):
    print('received message: '+str(data))
    emit('message', {'data': 'got it!'})


def getProcessList():
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        p = psutil.Process(proc.info['pid'])
        p.create_time()
        processlist.append({'pid': proc.info['pid'], 'name': proc.info['name'], 'username': proc.info['username'], 'uptime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p.create_time()))})

@socketio.on('getProcesses')
def handle_message(message):
    getProcessList()
    print('[Server socket]: ' + str(message))
    emit('processList', {'data': processlist})
    processlist.clear()

@socketio.on('getSystemInformation')
def handle_message(message):
    print('[Server socket]: ' + str(System_information()))
    emit('getSystemInformation', {'data': System_information()})

@socketio.on('getCpuInformation')
def handle_message(message):
    print('[Server socket]: ' + str(Cpu_information()))
    emit('getCpuInformation', {'data': Cpu_information()})

@socketio.on('getMemoryInformation')
def handle_message(message):
    print('[Server socket]: ' + str(Memory_information()))
    emit('getMemoryInformation', {'data': Memory_information()})

@socketio.on('getSwapInformation')
def handle_message(message):
    print('[Server socket]: ' + str(Swap_information()))
    emit('getSwapInformation', {'data': Swap_information()})

@socketio.on('getDiskInformation')
def handle_message(message):
    print('[Server socket]: ' + str(Disk_information()))
    emit('getDiskInformation', {'data': Disk_information()})    


@socketio.on('getViewedWebsiteInformation')
def handle_message(message):
    # print('[Server socket]: ' + str(Disk_information()))
    emit('getViewedWebsiteInformation', {'data': url_viewtime, 'data2': wwwtime})    
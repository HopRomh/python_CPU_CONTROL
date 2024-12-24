import psutil
import time 
import GPUtil
import logging


logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    filename='system_metrics.log', 
                    filemode='a')  


def translate_byts(bytest_value):
    for unit in['B', 'KB', 'MB', 'GB', 'TB']:
        if bytest_value < 1024: 
            return f"{bytest_value:.2f} {unit}"
        bytest_value /= 1024


def systemMetrics():
    # Процессор 
    cpu_usage = psutil.cpu_percent(interval=1)
    # Видео карта
    gpu = GPUtil.getGPUs()
    gpu_usage = [gpu.load * 100 for gpu in gpu]
    # Оперативка
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    # Использование диска
    disk_info = psutil.disk_usage('/')
    disk_usage = disk_info.percent
    # Сетевые данные
    net_info = psutil.net_io_counters()
    bytes_sent = net_info.bytes_sent
    bytes_recv = net_info.bytes_recv
    if gpu_usage:
        for i, usage in enumerate(gpu_usage):
            print(f"GPU {i}: {usage:.2f}%")
    else:
        print("Не онаружена видео карта.")


    print(f"Процессор: {cpu_usage}%")
    print(f"Видео карта: {gpu_usage}%")
    print(f"Оперативка: {memory_usage}%")
    print(f"Использование диска: {disk_usage}%")
    print(f"отправленное: {translate_byts(bytes_sent)}")
    print(f"полученон: {translate_byts(bytes_recv)}")
    print("-" * 45)


def system_metrics_warning(cpu_warning=80,gpu_warning=80, memory_warning=80,disk_warning=90): 
    cpu_usage = psutil.cpu_percent(interval=1)
    gpu = GPUtil.getGPUs()
    gpu_usage = [gpu.load * 100 for gpu in gpu]
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    disk_info = psutil.disk_usage('/')
    disk_usage = disk_info.percent
    if gpu_usage:
        for i, usage in enumerate(gpu_usage):
            if usage > gpu_warning:  
                print(f"⚠️ Warning! GPU {i} usage is high: {usage:.2f}%")
            else:
                print(f"GPU {i}: {usage:.2f}%")
    else:
        print("Не обнаружена видео карта.")
    
    if cpu_usage > cpu_warning:
        print(f"⚠️ Warning! CPU usage is high: {cpu_usage}%")
    if memory_usage > memory_warning:
        print(f"⚠️ Warning! CPU usage is high: {memory_usage}%")
    if disk_usage > disk_warning:
        print(f"⚠️ Warning! CPU usage is high: {disk_usage}%")
    return cpu_usage, gpu_usage, memory_usage, disk_usage
    

def logs(cpu_usage, gpu_usage, memory_usage, disk_usage):
    logMessage = f"Процессор: {cpu_usage}%, Видео карта: {gpu_usage}, Оперативка: {memory_usage}%, Использование диска: {disk_usage}%"
    logging.info(logMessage)

while True: 
    systemMetrics()
    cpu_usage, gpu_usage, memory_usage, disk_usage = system_metrics_warning()
    logs(cpu_usage, gpu_usage, memory_usage, disk_usage)
    time.sleep(5)
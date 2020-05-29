import psutil, os, time, numpy as np

def checkProcess(process):
    for proc in psutil.process_iter():
        if proc.name().upper() == process.upper():
            return True
    return False
                
while True:
    time.sleep(1)
    if checkProcess('comsolmphserver.exe'):
        print('Process is running, no need to launch.')
    else:
        time_wait = np.random.randint(60, 71)
        print(f'Process is not running. Waiting {time_wait} seconds...')
        time.sleep(time_wait)
        os.startfile(r"C:\Users\amscott3\Desktop\GRC Projects\COMSOL\COMSOL Multiphysics 5.5 with MATLAB")
        print("Launched.")
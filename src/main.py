from execute import execute
import datetime
import psutil
import os

if __name__ == '__main__':
    data_to_process = {
        'file': 'test/files/red_10.json',
        'future': 'ABC',
        'current': 'ABC',
        'state': '1000000000',
        'channels': 'ABCDEFGHIJ', # 10000000
        'method': 'delete_edges' # partition | delete_edges
    }

    #execute(data_to_process)
    
    try:
        # Capturar la hora de inicio
        hora_inicio = datetime.datetime.now()
        print("Hora de inicio:", hora_inicio)
            # Obtener el proceso actual
        proceso = psutil.Process(os.getpid())

        # Obtener el uso de recursos antes de ejecutar la función
        uso_inicial = proceso.memory_info().rss

        execute(data_to_process)
    
    except Exception as e:
        print(e)

    finally:
        # Capturar la hora de finalización
        hora_final = datetime.datetime.now()
        print("Hora de finalización:", hora_final)

        uso_final = proceso.memory_info().rss

        # Calcular el uso máximo de memoria (en bytes)
        uso_maximo_memoria = uso_final - uso_inicial
        uso_maximo_memoria = uso_maximo_memoria / (1024 ** 2)
        print(f"Uso máximo de memoria: {uso_maximo_memoria} Mbytes")

        # Calcular el uso de CPU
        uso_cpu = proceso.cpu_times()
        uso_maximo_cpu = uso_cpu.user + uso_cpu.system
        print(f"Uso máximo de CPU: {uso_maximo_cpu} segundos")

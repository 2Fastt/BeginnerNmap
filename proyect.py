import socket
import subprocess
import re
import sys
import asyncio
from colorama import init, Fore, Style
import platform
import concurrent.futures

init()

def imprimir_banner():
    banner = f"""
{Style.BRIGHT}{Fore.MAGENTA}░▒▓███████▓▒░░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓███████▓▒░▒▓███████▓▒░▒▓████████▓▒░ 
       ░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░         ░▒▓█▓▒░     
       ░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░         ░▒▓█▓▒░     
 ░▒▓██████▓▒░░▒▓██████▓▒░░▒▓████████▓▒░░▒▓██████▓▒░░▒▓██████▓▒░   ░▒▓█▓▒░     
░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░  ░▒▓█▓▒░     
░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░  ░▒▓█▓▒░     
░▒▓████████▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░▒▓███████▓▒░   ░▒▓█▓▒░     
                                                                                                                     
    """
    firma = f"{Style.BRIGHT}{Fore.GREEN}Made by: 2Fasst{Style.RESET_ALL}"
    banner_con_firma = banner + firma.rjust(len(banner.split("\n")[-1]))
    print(banner_con_firma)

imprimir_banner()

def imprimir_scan_completado():
    mensaje = f"{Style.BRIGHT}{Fore.GREEN}Scan Completado!!{Style.RESET_ALL}"
    print(mensaje)

async def escaneodepuertos(puerto):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        resultado = s.connect_ex((objetivo, puerto))
        if resultado == 0:
            protocolos = []
            for proto in ['TCP', 'UDP', 'SCTP', 'ICMP', 'igmp', 'HTTP', 'HTTPS', 'SMTP']:
                try:
                    servicio = socket.getservbyport(puerto, proto)
                    protocolos.append(proto)
                except OSError:
                    pass
            if protocolos:
                print(f"Puerto {puerto} abierto. Protocolos: {', '.join(protocolos)}")
        s.close()
    except:
        pass

async def scanear_puertos():
    total_puertos = 65535
    with concurrent.futures.ProcessPoolExecutor() as executor:
        await asyncio.gather(*(escaneodepuertos(puerto) for puerto in range(1, total_puertos + 1)))

def verificar_ip_valida(ip):
    patron_ip = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    return re.match(patron_ip, ip) is not None

def verificar_conectividad(ip):
    try:
        sistema_operativo = platform.system()
        if sistema_operativo == "Windows":
            resultado = subprocess.run(["ping", "-n", "1", ip], capture_output=True, text=True, timeout=5)
        else:
            resultado = subprocess.run(["ping", "-c", "1", ip], capture_output=True, text=True, timeout=5)
        
        if resultado.returncode == 0:
            print("Conexión exitosa. Escaneando puertos...")
            return True
        else:
            print("No se pudo establecer conexión con la dirección IP.")
            return False
    except Exception as e:
        print(f"Error al verificar la conectividad: {e}")
        return False

if __name__ == '__main__':
    ip = input("Inserte la dirección IP: ")

    if not verificar_ip_valida(ip):
        print("La dirección IP ingresada no es válida.")
        sys.exit()

    if not verificar_conectividad(ip):
        print("No se puede establecer conexión con la dirección IP. Programa terminado.")
        sys.exit()

    objetivo = socket.gethostbyname(ip)

    asyncio.run(scanear_puertos())

    imprimir_scan_completado()

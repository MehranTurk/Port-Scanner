import os
import socket
import getpass
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style

def save_ips_to_file(ips):
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    file_path = os.path.join(desktop_path, 'ip.txt')
    with open(file_path, 'w') as f:
        for ip in ips:
            f.write(ip + '\n')
    print(f"IP addresses saved to {file_path}")

def main():
    try:
        ip_range = input("Enter IP range (e.g., 192.168.1.1-10): ")
        start_ip, end_ip = ip_range.split('-')
        start_ip = start_ip.strip()
        end_ip = end_ip.strip()
        
        start_port = int(input("Enter starting port: "))
        end_port = int(input("Enter ending port: "))
        
        open_ips = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(scan_ports, start_ip, i, start_port, end_port) for i in range(int(start_ip.split('.')[-1]), int(end_ip.split('.')[-1])+1)]
            for future in futures:
                result = future.result()
                if result[1]:
                    open_ips.append(result[0])
                    print(f"{Fore.GREEN}Open ports on {result[0]}: {', '.join(map(str, result[1]))}{Style.RESET_ALL}")
                else:
                    print(f"No open ports on {result[0]}")

        save_ips_to_file(open_ips)

    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
    except Exception as e:
        print(f"Error occurred: {e}")

def scan_ports(ip, i, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                sock.connect((ip.rsplit('.', 1)[0] + '.' + str(i), port))
                open_ports.append(port)
        except socket.timeout:
            pass
        except Exception as e:
            print(f"Error occurred: {e}")
    return (ip.rsplit('.', 1)[0] + '.' + str(i), open_ports)

if __name__ == "__main__":
    main()

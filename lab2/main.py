import subprocess
import sys
import re
import platform

HEADERS_SIZE = 28
MAX_MTU_VALUE = 1500
ICMP_CONFIG_PATH = "/proc/sys/net/ipv4/icmp_echo_ignore_all"

def exit_with_message(message, code=1):
    print(message)
    exit(code)

def perform_ping(host, packet_size, timeout=3000):
    os_command = 'darwin' if platform.system().lower() == 'darwin' else 'linux'
    if os_command == 'darwin':
        command = f'ping -D -s {packet_size} -c 1 -W {timeout} {host}'
    else:
        command = f'ping -M do -s {packet_size} -c 1 -W {timeout // 1000} {host}'
    result = subprocess.run(command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def binary_search_mtu(host):
    left, right = 0, MAX_MTU_VALUE
    while left + 1 < right:
        mid = (left + right) // 2
        if perform_ping(host, mid):
            print(f"MTU {mid} is ok")
            left = mid
        else:
            print(f"MTU {mid} is bad")
            right = mid
    return left

if len(sys.argv) < 2:
    exit_with_message("Usage: python3 main.py <host>")

host = sys.argv[1]
HOST_PATTERN = re.compile(
    r"^(https?:\/\/)?((?:[-a-z0-9._~!$&\'()*+,;=]|%[0-9a-f]{2})+(?::(?:[-a-z0-9._~!$&\'()*+,;=]|%[0-9a-f]{2})+)?@)?(?:((?:(?:\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3}(?:\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]))|((?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z][a-z0-9-]*[a-z0-9]))(:\d+)?((?:\/(?:[-a-z0-9._~!$&\'()*+,;=:@]|%[0-9a-f]{2})+)*\/?)(\?(?:[-a-z0-9._~!$&\'()*+,;=:@\/?]|%[0-9a-f]{2})*)?(\#(?:[-a-z0-9._~!$&\'()*+,;=:@\/?]|%[0-9a-f]{2})*)?$"
)

if not HOST_PATTERN.match(host):
    exit_with_message(f"Invalid host format: {host}")

print(f'Checking MTU for host: {host}')

if platform.system().lower() == 'linux':
    try:
        with open(ICMP_CONFIG_PATH, 'r') as file:
            if file.read().strip() == "1":
                exit_with_message("ICMP is disabled. Modify ICMP settings to proceed.", 1)
    except FileNotFoundError:
        pass

if not perform_ping(host, 0):
    exit_with_message(f"Host {host} is unreachable", 0)

minimal_mtu = binary_search_mtu(host)
print(f"Minimal MTU for {host} = {minimal_mtu}")
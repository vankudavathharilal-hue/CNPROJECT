import socket
import time
from ping3 import ping


def ping_host(host):
    """Check reachability and measure ICMP-style ping latency."""
    try:
        latency = ping(host, timeout=2, unit="ms")

        if latency is None:
            return {
                "host": host,
                "status": "OFFLINE",
                "latency": None
            }

        return {
            "host": host,
            "status": "ONLINE",
            "latency": round(float(latency), 2)
        }

    except Exception as exc:
        return {
            "host": host,
            "status": "ERROR",
            "latency": None,
            "error": str(exc)
        }


def dns_lookup(host):
    """Resolve a hostname to an IPv4 address."""
    try:
        ip = socket.gethostbyname(host)

        return {
            "host": host,
            "ip": ip,
            "status": "RESOLVED"
        }

    except socket.gaierror:
        return {
            "host": host,
            "ip": None,
            "status": "FAILED"
        }


def tcp_check(host, port=443):
    """Test whether a TCP port is reachable."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)

    try:
        start = time.perf_counter()
        result = sock.connect_ex((host, port))
        latency = (time.perf_counter() - start) * 1000

        if result == 0:
            return {
                "host": host,
                "port": port,
                "status": "OPEN",
                "latency": round(latency, 2)
            }

        return {
            "host": host,
            "port": port,
            "status": "CLOSED",
            "latency": None
        }

    except Exception as exc:
        return {
            "host": host,
            "port": port,
            "status": "ERROR",
            "latency": None,
            "error": str(exc)
        }

    finally:
        sock.close()

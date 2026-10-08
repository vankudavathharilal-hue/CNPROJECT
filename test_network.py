from network_monitor import ping_host, dns_lookup, tcp_check

HOST = "google.com"

print("\n--- PING TEST ---")
print(ping_host(HOST))

print("\n--- DNS TEST ---")
print(dns_lookup(HOST))

print("\n--- TCP TEST ---")
print(tcp_check(HOST, 443))

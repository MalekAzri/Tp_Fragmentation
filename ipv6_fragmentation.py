from scapy.all import *
import os


DST_IPV6 = "<IPV6_WINDOWS>"


print("[+] Test de connectivité IPv6")
os.system(f"ping6 -c 3 {DST_IPV6}")


payload = b"B" * 4000


# ----- AVEC FRAGMENTATION -----
pkt_frag = IPv6(dst=DST_IPV6)/IPv6ExtHdrFragment()/ICMPv6EchoRequest()/payload
print("[+] IPv6 avec Fragment Header")
send(pkt_frag)


# ----- SANS FRAGMENTATION -----
pkt_no_frag = IPv6(dst=DST_IPV6)/ICMPv6EchoRequest()/payload
print("[+] IPv6 sans Fragment Header (échec attendu si MTU dépassée)")
send(pkt_no_frag)
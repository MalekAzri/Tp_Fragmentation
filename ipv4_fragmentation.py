from scapy.all import *
import os


DST_IP = "<IP_DESTINATION>"


print("[+] Test de connectivité IPv4")
os.system(f"ping -c 3 {DST_IP}")


payload = b"A" * 4000


# ----- AVEC FRAGMENTATION -----
pkt_frag = IP(dst=DST_IP)/ICMP()/payload
fragments = fragment(pkt_frag, fragsize=1480)
print(f"[+] IPv4 avec fragmentation : {len(fragments)} fragments")
send(fragments)


# ----- SANS FRAGMENTATION (DF=1) -----
pkt_df = IP(dst=DST_IP, flags="DF")/ICMP()/payload
print("[+] IPv4 sans fragmentation (DF=1)")
send(pkt_df)
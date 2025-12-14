#!/usr/bin/env python3
"""
Script d'analyse des paquets pour la simulation de fragmentation IPv4 et IPv6.
Utilise Scapy pour capturer et analyser les paquets ICMP/IPv4 et ICMPv6/IPv6.
"""

from scapy.all import *
import sys

def analyze_ipv4_packets(pkt):
    """
    Analyse un paquet IPv4 pour fragmentation.
    """
    if IP in pkt and ICMP in pkt:
        ip = pkt[IP]
        icmp = pkt[ICMP]
        print(f"[IPv4] Paquet capturé: {ip.src} -> {ip.dst}")
        print(f"  Taille totale: {len(pkt)} octets")
        print(f"  ID: {ip.id}")
        print(f"  Flags: DF={ip.flags.DF}, MF={ip.flags.MF}")
        print(f"  Fragment Offset: {ip.frag}")
        if ip.flags.MF or ip.frag > 0:
            print("  -> Fragment détecté")
        else:
            print("  -> Paquet non fragmenté")
        print(f"  Payload ICMP: {len(icmp.payload)} octets")
        print("-" * 50)

def analyze_ipv6_packets(pkt):
    """
    Analyse un paquet IPv6 pour fragmentation.
    """
    if IPv6 in pkt and ICMPv6EchoRequest in pkt:
        ipv6 = pkt[IPv6]
        icmpv6 = pkt[ICMPv6EchoRequest]
        print(f"[IPv6] Paquet capturé: {ipv6.src} -> {ipv6.dst}")
        print(f"  Taille totale: {len(pkt)} octets")
        if IPv6ExtHdrFragment in pkt:
            frag = pkt[IPv6ExtHdrFragment]
            print(f"  Fragment Header détecté (Next Header: {frag.nh})")
            print(f"  Identification: {frag.id}")
            print(f"  Fragment Offset: {frag.offset}")
            print(f"  More Fragments (M): {frag.m}")
            print("  -> Fragment IPv6")
        else:
            print("  -> Pas de Fragment Header (paquet non fragmenté)")
        print(f"  Payload ICMPv6: {len(icmpv6.payload)} octets")
        print("-" * 50)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 packet_analysis.py <ipv4|ipv6> [interface]")
        print("Exemple: python3 packet_analysis.py ipv4 eth0")
        sys.exit(1)

    protocol = sys.argv[1].lower()
    interface = sys.argv[2] if len(sys.argv) > 2 else "any"

    print(f"Démarrage de l'analyse des paquets {protocol.upper()} sur interface {interface}")
    print("Appuyez sur Ctrl+C pour arrêter.")

    try:
        if protocol == "ipv4":
            # Filtre pour IPv4 ICMP
            sniff(iface=interface, prn=analyze_ipv4_packets, filter="ip and icmp", store=0)
        elif protocol == "ipv6":
            # Filtre pour IPv6 ICMPv6
            sniff(iface=interface, prn=analyze_ipv6_packets, filter="ip6 and icmp6", store=0)
        else:
            print("Protocole invalide. Utilisez 'ipv4' ou 'ipv6'.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nAnalyse arrêtée.")
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    main()
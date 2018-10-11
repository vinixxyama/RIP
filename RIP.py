# - Alunos:
#       Renato Correa RA:620211
#       Vinicius Yamamoto RA:490105
#
# - Disciplina:
#       Laboratorio de redes
#
# - Professo:
#       Fabio Verdi
#
# - UFSCar Sorocaba

# ------ Libraries ------ #
import config
import mod
import sys
import socket
import threading
import struct
import time
from time import sleep
from thread import *

pid = 0
tabeladist = []
MCAST_ADDR = "224.0.0.251"
MCAST_PORT = 1050

# AF_INET: Specifies the use of (host, port) pair
# SOCK_DGRAM: Socket type, datagram
# IPPROTO_UDP: UDP Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# iinet_aton(): Convert the given address to 32-bit binary format
group = socket.inet_aton(MCAST_ADDR)

# INADDR_ANY: Bind socket to all local interfaces
mreq = struct.pack('4sL', group, socket.INADDR_ANY)

# IP_ADD_MEMBERSHIP: join the local multicast group
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# SO_REUSEADDR: Allow reuse of local address
# SO_REUSEPORT: Allow multiple sockets to be bound to same address
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

# IP_MULTICAST_LOOP: Loop the message to yourself
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

# Binds the socket
sock.bind(("224.0.0.251", 1050))

class rtpkt:
    mincost = []
    def __init__(self, sourceid, destid, mincost):
        self.sourceid = sourceid
        self.destid = destid
        self.mincost = mincost

class rip:
    def __init__(self,dist,nexthope):
        self.dist = dist
        self.nexthope = nexthope

def sender():
    # multicast the message to the given address
    buffer = str(pid) + "/"
    for i in tabeladist:
        buffer = buffer + str(i.dist) + "/" + str(i.nexthope) + "/"
    sock.sendto(buffer, ("224.0.0.251", 1050))


def receiver():
    tabledist = []
    while True:
        data = ""
        data = sock.recv(1024)
        rcvtable = data.split("/")
        for i in range(0,len(rcvtable)/2):
            tabledist.append(rcvtable[i*2+1])
        if(pid == 0):
            rtupdate0(rtpkt(rcvtable[0], pid, tabledist))
        if(pid == 1):
            rtupdate1(rtpkt(rcvtable[0], pid, tabledist))
        if(pid == 2):
            rtupdate2(rtpkt(rcvtable[0], pid, tabledist))
        if(pid == 3):
            rtupdate3(rtpkt(rcvtable[0], pid, tabledist))
        if(config.senderflag == 1):
            sender()
            config.senderflag = 0

def rtinit0():
    MCAST_ADDR = "224.0.0.251"
    MCAST_PORT = 1050
    tabeladist.append(rip(0, -1))
    tabeladist.append(rip(1, -1))
    tabeladist.append(rip(3, -1))
    tabeladist.append(rip(7, -1))


def rtinit1():
    MCAST_ADDR = "224.0.1.251"
    MCAST_PORT = 1051
    tabeladist.append(rip(1, -1))
    tabeladist.append(rip(0, -1))
    tabeladist.append(rip(1, -1))
    tabeladist.append(rip(999, -1))

def rtinit2():
    MCAST_ADDR = "224.0.2.251"
    MCAST_PORT = 1052
    tabeladist.append(rip(3, -1))
    tabeladist.append(rip(1, -1))
    tabeladist.append(rip(0, -1))
    tabeladist.append(rip(2, -1))

def rtinit3():
    MCAST_ADDR = "224.0.3.251"
    MCAST_PORT = 1053
    tabeladist.append(rip(7, -1))
    tabeladist.append(rip(999, -1))
    tabeladist.append(rip(2, -1))
    tabeladist.append(rip(0, -1))

def rtupdate0(rcvpkt):
    flag = 0
    for i in range(0,4):
        if(int(rcvpkt.sourceid) != pid and int(rcvpkt.mincost[i])+tabeladist[int(rcvpkt.sourceid)].dist < tabeladist[i].dist):
            tabeladist[i].dist = int(rcvpkt.mincost[i])+tabeladist[int(rcvpkt.sourceid)].dist
            tabeladist[i].nexthope = int(rcvpkt.sourceid)
            print ("Mudou a tabela")
            config.senderflag = 1
            flag = 1
    if(flag == 1):
        for i in range(0,4):
            print (str(tabeladist[i].dist) + " " + str(tabeladist[i].nexthope))

def rtupdate1(rcvpkt):
    flag = 0
    for i in range(0,4):
        if(int(rcvpkt.sourceid) != pid and int(rcvpkt.mincost[i])+tabeladist[int(rcvpkt.sourceid)].dist < tabeladist[i].dist):
            tabeladist[i].dist = int(rcvpkt.mincost[i])+tabeladist[int(rcvpkt.sourceid)].dist
            tabeladist[i].nexthope = int(rcvpkt.sourceid)
            print ("Mudou a tabela")
            config.senderflag = 1
            flag = 1
    if(flag == 1):
        for i in range(0,4):
            print (str(tabeladist[i].dist) + " " + str(tabeladist[i].nexthope))

def rtupdate2(rcvpkt):
    flag = 0
    for i in range(0,4):
        if(int(rcvpkt.sourceid) != pid and int(rcvpkt.mincost[i])+tabeladist[int(rcvpkt.sourceid)].dist < tabeladist[i].dist):
            tabeladist[i].dist = int(rcvpkt.mincost[i])+tabeladist[int(rcvpkt.sourceid)].dist
            tabeladist[i].nexthope = int(rcvpkt.sourceid)
            print ("Mudou a tabela")
            config.senderflag = 1
            flag = 1
    if(flag == 1):
        for i in range(0,4):
            print (str(tabeladist[i].dist) + " " + str(tabeladist[i].nexthope))

def rtupdate3(rcvpkt):
    flag = 0
    for i in range(0,4):
        if(int(rcvpkt.sourceid) != pid and int(rcvpkt.mincost[i])+tabeladist[int(rcvpkt.sourceid)].dist < tabeladist[i].dist):
            tabeladist[i].dist = int(rcvpkt.mincost[i])+tabeladist[int(rcvpkt.sourceid)].dist
            tabeladist[i].nexthope = int(rcvpkt.sourceid)
            print ("Mudou a tabela")
            config.senderflag = 1
            flag = 1
    if(flag == 1):
        for i in range(0,4):
            print (str(tabeladist[i].dist) + " " + str(tabeladist[i].nexthope))

if __name__ == '__main__':
    pid = int(sys.argv[1])
    if(sys.argv[1] == str(0)):
        rtinit0()
    if(sys.argv[1] == str(1)):
        rtinit1()
    if(sys.argv[1] == str(2)):
        rtinit2()
    if(sys.argv[1] == str(3)):
        rtinit3()

    for a in tabeladist:
        print(str(a.dist) + " " + str(a.nexthope))

    r = threading.Thread(target = receiver)
    #s = threading.Thread(target = sender)

    r.daemon = True
    #s.daemon = True

    r.start()
    #s.start()
    opcao = raw_input("Deseja enviar uma mensagem? ")
    if(int(opcao) == 3):
        sender()
    while(True):
        time.sleep(1)


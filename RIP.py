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
tabelaoriginal = []
MCAST_ADDR = "224.0.0.251"
MCAST_PORT = 1050
ip0 = "224.0.0.251"
ip1 = "224.0.1.251"
ip2 = "224.0.2.251"
ip3 = "224.0.3.251"
#sender
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#receiver
sock0 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock3 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

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
        if(tabelaoriginal[0].dist != 999 and tabelaoriginal[0].dist != 0):
            sock.sendto(buffer, (ip0, 1050))
        if(tabelaoriginal[1].dist != 999 and tabelaoriginal[1].dist != 0):
            sock.sendto(buffer, (ip1, 1050))
        if(tabelaoriginal[2].dist != 999 and tabelaoriginal[2].dist != 0):
            sock.sendto(buffer, (ip2, 1050))
        if(tabelaoriginal[3].dist != 999 and tabelaoriginal[3].dist != 0):
            sock.sendto(buffer, (ip3, 1050))


def receiver():
    while True:
        tabledist = []
        data = ""
        data = sock.recv(1024)
        rcvtable = data.split("/")
        print("tcvpid:", rcvtable[0])
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
    tabeladist.append(rip(0, -1))
    tabeladist.append(rip(1, -1))
    tabeladist.append(rip(3, -1))
    tabeladist.append(rip(7, -1))
    sock0.bind((ip0, 1050))
    for i in range(0,4):
        tabelaoriginal.append(tabeladist[i])
        


def rtinit1():
    tabeladist.append(rip(1, -1))
    tabeladist.append(rip(0, -1))
    tabeladist.append(rip(1, -1))
    tabeladist.append(rip(999, -1))
    sock0.bind((ip1, 1050))
    for i in range(0,4):
        tabelaoriginal.append(tabeladist[i])

def rtinit2():
    tabeladist.append(rip(3, -1))
    tabeladist.append(rip(1, -1))
    tabeladist.append(rip(0, -1))
    tabeladist.append(rip(2, -1))
    sock0.bind((ip2, 1050))
    for i in range(0,4):
        tabelaoriginal.append(tabeladist[i])

def rtinit3():
    tabeladist.append(rip(7, -1))
    tabeladist.append(rip(999, -1))
    tabeladist.append(rip(2, -1))
    tabeladist.append(rip(0, -1))
    sock0.bind((ip3, 1050))
    for i in range(0,4):
        tabelaoriginal.append(tabeladist[i])

def rtupdate0(rcvpkt):
    flag = 0
    for i in range(0,4):
        if(int(rcvpkt.sourceid) != pid and int(rcvpkt.mincost[i])+tabeladist[int(rcvpkt.sourceid)].dist < tabeladist[i].dist):
            tabeladist[i].dist = int(rcvpkt.mincost[i])+tabeladist[int(rcvpkt.sourceid)].dist
            if(tabeladist[int(rcvpkt.sourceid)].nexthope != -1):
                tabeladist[i].nexthope = tabeladist[int(rcvpkt.sourceid)].nexthope
            else:
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
            if(tabeladist[int(rcvpkt.sourceid)].nexthope != -1):
                tabeladist[i].nexthope = tabeladist[int(rcvpkt.sourceid)].nexthope
            else:
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
            if(tabeladist[int(rcvpkt.sourceid)].nexthope != -1):
                tabeladist[i].nexthope = tabeladist[int(rcvpkt.sourceid)].nexthope
            else:
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
            if(tabeladist[int(rcvpkt.sourceid)].nexthope != -1):
                tabeladist[i].nexthope = tabeladist[int(rcvpkt.sourceid)].nexthope
            else:
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


# -*- coding: utf-8 -*-
import requests
import xml.etree.ElementTree as ET
import time
import os

supportPerson = "Lasse Gøransson"
scTerm = "lasse"
soundfile = "muttley.mp3"
refreshRate = 20 #secs


class Ticket:

    def __init__(self):
        self.headline = ""
        self.supportPerson = ""
        self.inc = ""
        self.status = ""
        self.servicecomment = ""



def playSound():
   freg = 350
   for x in xrange(2):
        os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 0.1, freg))
        freg += 300

def playSoundFile(soundfile):
    os.system('cvlc '+soundfile+' --play-and-exit 2> /dev/null')




playSoundFile(soundfile)
tickets = []

while True:
     prevNum = len(tickets)
     # Get all cases from the servicedesk

     r = requests.get('http://10.80.0.135/api/public/index.php/efecte/get/sd/506185')

     root = ET.fromstring(r.text.encode('utf-8'))

     numTickets = 0
     tickets = []
     for child in root:
         save = False
         newTicket = Ticket()
         numTickets += 1
         for attr in child:

             if 'code' in attr.attrib:
                 if attr.attrib['code'] == "support_person":
                     for value in attr:
                         if value.attrib['name'] == supportPerson.decode('latin1'):
                             newTicket.supportPerson = value.attrib['name']
                             save = True

                 if attr.attrib['code'] == "service_comment":
                     for value in attr:
                         if scTerm.lower() in value.text.lower():
                             newTicket.servicecomment = value.text
                             save = True


                 if attr.attrib['code'] == "subject":
                     for value in attr:
                         newTicket.headline = value.text

                 if attr.attrib['code'] == "status":
                     for value in attr:
                         newTicket.status = value.text

                 if attr.attrib['code'] == "efecte_id_copy":
                     for value in attr:
                         newTicket.inc = value.text









         if save:
             tickets.append(newTicket)

     if prevNum < len(tickets):
         print '############## Ny sag #################'
         playSound()


     print "Previous: %s Now: %s at: %s" % (prevNum,len(tickets),str(time.strftime("%H:%M:%S")))

     time.sleep(refreshRate)

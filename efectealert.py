# -*- coding: utf-8 -*-
import requests
import xml.etree.ElementTree as ET
from ticket import Ticket
import time
import os
import sys



def playSound():
    os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 0.1, 1000))
    os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 0.1, 1100))
    os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 0.1, 1200))
    os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 0.1, 1100))
    os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 0.1, 1000))
    os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 0.1, 900))

tickets = []

while True:
    prevNum = len(tickets)
    # Get all cases from the servicedesk

    r = requests.get('https://servicedesk.sdu.dk/efecte/search.ws?query=SELECT%20entity%20FROM%20entity%20WHERE%20referenceData.groupAttribute.code%20=%20%27support_group%27%20AND%20referenceData.target.id%20=%20%27506185%27%20AND%20template.id%20=%20%2736%27%20AND%20entity.hidden%20=%20false%20AND%20entity.deleted%20=%20false',auth=('servicevagt','servicevagt'))

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
                        if value.attrib['name'] == "Lasse Gøransson".decode('utf-8'):
                            newTicket.supportPerson = value.attrib['name']
                            save = True

                if attr.attrib['code'] == "service_comment":
                    for value in attr:
                        if "Lasse".lower() in value.text.lower():
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


    print "Previous: %s Now: %s" % (prevNum,len(tickets))

    time.sleep(5)
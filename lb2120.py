#!/usr/bin/python
#
# uses the web UI of the LB2120 to retrieve useful json from its internal API
#
helpstr='Usage:  lb2120.py -p password -i ipaddress -o jsonobject -k jsonkey\n' \
'                  -p password -i ipaddress -n number -t text\n' \
'                  -p password -i ipaddress -r (restart)\n'
#

from lxml import html
from lxml import etree
import requests
import json
import random
import sys,getopt

argv = sys.argv[1:]

IP='192.168.5.1'
password=''
jsonkey=''
jsonobject=''
phonenumber=''
restart='false'

try:
    opts, args = getopt.getopt(argv,'hri:p:o:k:n:t:',['ip=','password=','object=','key=','number=','text='])
except getopt.GetoptError:
    print (helpstr)
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print (helpstr)
        sys.exit()
    elif opt in ("-p","--password"):
        password = arg
    elif opt in ("-i","--ip"):
        IP = arg
    elif opt in ("-k","--key"):
        jsonkey = arg
    elif opt in ("-o","--object"):
        jsonobject = arg
    elif opt in ("-n","--number"):
        phonenumber = arg
    elif opt in ("-t","--text"):
        textmessage = arg
    elif opt in ("-r","--restart"):
        restart = 'true'

if not password:
    print ('Password required.\n\n' + helpstr)
    sys.exit(2)

if ( restart == 'true' ) and (( phonenumber != '') or ( jsonkey != '') or ( jsonobject != '')):
    print ('Restart cannot be combined with other options.\n\n' + helpstr)
    sys.exit(2)

REQUEST_URL = 'http://' + IP + '/index.html'

with requests.Session() as session:
    r = session.get(REQUEST_URL)
    form_page = html.fromstring(r.content)

    token = form_page.forms[0].fields['token']

    form = form_page.forms[1]

    form.fields['session.password'] = password
    form.action = 'http://' + IP + form.action
    postdata = form.form_values()
    postdata.append(('token',token))
    r = session.post(form.action,data=postdata)

    if restart=='true':
        restartform = form_page.forms[1]
        postdata = restartform.form_values()
        postdata.append(('general.routerReset', '1'))
        postdata.append(('token',token))
        postdata.append(('general.shutdown','Restart'))
        r = session.post(restartform.action,data=postdata)
        print ('Restarted')

    elif phonenumber:

        smsform = form_page.forms[2]
        smsform.fields['sms.sendMsg.receiver'] = phonenumber
        smsform.fields['sms.sendMsg.text'] = textmessage
        smsform.action = 'http://' + IP + smsform.action
        postdata = smsform.form_values()
        postdata.append(('sms.sendMsg.clientId','test'))
        postdata.append(('action','send'))
        postdata.append(('token',token))
        r = session.post(smsform.action,data=postdata)
        print ('Sent')

    else:

        api_url = 'http://' + IP + '/api/model.json?internalapi=1&x=' + str(random.randint(1,100000))

        r = session.get(api_url, headers={'referer': REQUEST_URL,'dnt': '1','host': '192.168.5.1'})

        json_object=json.loads(r.content)

        if jsonkey:
            print(json_object[jsonobject][jsonkey])
        elif jsonobject:
            print(json_object[jsonobject])
        else:
            print(json.dumps(json_object, indent=1))


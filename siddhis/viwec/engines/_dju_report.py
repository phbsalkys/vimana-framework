# -*- coding: utf-8 -*-

from pygments.formatters import TerminalFormatter
import sys, re, os, random, string, platform
from lxml.html.soupparser import fromstring
from pygments.lexers import PythonLexer
from neotermcolor import cprint, colored
from prettytable import PrettyTable
from collections import OrderedDict 
from pygments import highlight
from bs4 import BeautifulSoup
from netaddr import IPNetwork
from datetime import datetime
from time import sleep
import pygments
import argparse
import hashlib
import yaml


from settings.siddhis_shared_settings import django_envvars as djev
from settings.siddhis_shared_settings import csrf_table as csrf
from settings.siddhis_shared_settings import set_header 
from settings.siddhis_shared_settings import api_auth
from settings.siddhis_shared_settings import payloads
from core.vmnf_shared_args import VimanaSharedArgs
from core.vmnf_thread_handler import ThreadPool
import settings.vmnf_settings as settings
from core.vmnf_pshell import vmnfshell

from res.session.vmnf_sessions import createSession
from res.vmnf_text_utils import format_text
from res.vmnf_pxh import exception_hierarchy
from res import vmnf_banners
from res import colors

from requests import exceptions
from random import choice
import collections
import requests

from . _dju_settings import table_models
from siddhis.tictrac import tictrac
from . _dju_utils import DJUtils
from siddhis.prana import prana


class resultParser:   
    def __init__(self, results, **vmnf_handler):
        # dmt handler (argparser namespace) 
        self.vmnf_handler = vmnf_handler
        self.catched_exceptions = []

        self.fuzz_report=False
        tables = DJUtils().get_report_tables()
        
        self.exceptions_tbl = tables['exceptions']
        self.config_issues_tbl = tables['configuration']
        self.summary_tbl = tables['summary']
        self.tickets_tbl = tables['tickets']
        self.envleak_tbl = tables['envleak']
        self.cves_tbl = tables['cves']
        self.traceback_objects_tbl = tables['objects']

        # siddhi name
        self.vmnf_handler = vmnf_handler 
        self.siddhi = vmnf_handler['module_run'].lower()

        # results from djunch fuzzer 
        if (len(results['EXCEPTIONS'])) == 0:
            return None
        
        # instance of djunch results
        self.fuzz_report = results 
        
        # exception sampler: to use shared information between exceptions
        self.sampler = results['EXCEPTIONS'][0]

        # general analysis objects
        self.general_objects = results['GENERAL_OBJECTS']
        
        # mapped (expanded url patterns from DMT)
        self.raw_patterns = self.vmnf_handler['raw_patterns']
       
        # passive fingerprint results
        self.fingerprint = self.vmnf_handler['fingerprint']

    def show_issues(self):
        print("\033c", end="")
        vmnf_banners.audit_report_banner()
        
        if not self.fuzz_report:
            print('[result_parser: {}] Missing fuzzing result after {} execution'.format(
                datetime.now(),
                self.siddhi
                )
            )
    
            return False

        mark_status = colored(' ● ', 'green', attrs=['bold', 'blink'])
        status_msg = colored('Consolidating analysis result...', 'blue')
        print('\n {} {}'.format(mark_status, status_msg))
        sleep(1)
        
        security_tickets=None
        cves=None
        found_exceptions= [] 

        for exception in self.fuzz_report['EXCEPTIONS']:
            found_exceptions.append(exception['EXCEPTION_TYPE'].rstrip())

        pxh = exception_hierarchy()
        for x in pxh.split('\n'):
            x_ref = (x.split('- ')[-1])
            if x_ref in found_exceptions:
                x_c = colored(x_ref,'red',attrs=['bold','blink'])
                x = x.replace(x_ref,x_c)
            print(x)
            sleep(0.10)
        sleep(1)

        _prana_ = []
        cve_siddhi = colored('prana', 'green')
        tickets_siddhi = colored('tictrac', 'green') 
        
        if self.sampler['EXCEPTION_SUMMARY'].get('Django Version'):
            x_summary = self.sampler['EXCEPTION_SUMMARY']
            django_version = x_summary.get('Django Version').strip()
            
            installed_items = self.sampler['INSTALLED_ITEMS']
            
            # if Django Versions is found in Djunch 'environment_context'
            if django_version and django_version is not None:
                if len(django_version.split('.')) >= 3:
                    django_version = '.'.join(django_version.split('.')[:-1])
                '''    
                # if dmt already retrieve sec issues through passive fingerprint
                if django_version == self.fingerprint.get('flag_version'):
                    if self.fingerprint.get('cves'):
                        cves = self.fingerprint.get('cves')
                    
                    if self.fingerprint.get('tcts'):
                        security_tickets = self.fingerprint.get('tcts')
                else:
                    # - Get CVEs and security tickets for abducted framework version-
                    #security_tickets = tictrac.siddhi(django_version).start()
                    #cves = prana.siddhi(django_version).start()
                    pass
                '''
                if security_tickets is not None:
                    #and security_tickets is not None: 
                
                    # Security Tickets table
                    for ticket in security_tickets:
                        title = ticket['title']
                    
                        # max text len to pretty result
                        if len(title) > 100:
                            title = str(title[:100]) + '...'
                    
                        # >> load security tickets 
                        self.tickets_tbl.title = colored(
                            "Security tickets for Django {}".format(django_version),
                            "white", attrs=['bold']
                        )

                        self.tickets_tbl.add_row(
                            [
                                colored('ST{}'.format(ticket['id']),'green'),
                                title
                            ]
                        )
                else:
                    self.tickets_tbl = '?'
                    
                  
                # CVE table
                if cves is not None:
                    for entry in cves:
                        # >> load cve ids
                        self.cves_tbl.title = colored(
                            "CVE IDs for Django {}".format(django_version),
                            "white",attrs=['bold']
                        )
                    
                        self.cves_tbl.add_row(
                            [
                                colored(entry['id'],'green'),
                                entry['title'].rstrip(),
                                entry['date'].rstrip()

                            ]
                        )
                else:self.cves_tbl = '?'

        # issues overview
        self.issues_overview = {
            'total_issues': (
                len(self.fuzz_report['EXCEPTIONS']) + \
                len(self.fuzz_report['CONFIGURATION'])),
            'objects': len(self.general_objects),
            'security_tickets': len(security_tickets) if security_tickets else 0,
            'cve_ids': len(cves) if cves else 0,
            'url_patterns': len(self.raw_patterns) if self.raw_patterns else 0,   
            'applications': len(installed_items.get('Installed Applications')),
            'middlewares' : len(installed_items.get('Installed Middlewares'))
        }

        for tb_object in self.general_objects:
            self.traceback_objects_tbl.add_row(
                [
                    tb_object['variable'],
                    tb_object['object'],
                    colored(tb_object['address'], 'blue')
                ]
            )

        i_count = 1
        # >> load contexts 
        self.contexts = self.sampler['CONTEXTS']
        for k,v in self.contexts.items():
            self.envleak_tbl.add_row(
                [
                    colored('LC{}'.format(str(i_count)), 'green'),
                    k.strip(),
                    str(len(self.contexts[k]))
                ]
            )

            i_count +=1

        # dmt isnot using this table yet
        # >> load issues summary
        self.summary_tbl.add_row(
            [
                self.issues_overview['total_issues'],
                self.issues_overview['security_tickets'],
                self.issues_overview['cve_ids']
            ]
        )

        i_count = 1
        
        # >> load exceptions into table 
        env_pool = []
        count_lines = False
        count_vars  = False
        count_triggers = False
        total_xocc = False

        for exception in self.fuzz_report['EXCEPTIONS']:
            x_traceback = exception['EXCEPTION_TRACEBACK']
            env_count = len(exception['ENVIRONMENT'])
            occ_count = exception['EXCEPTION_COUNT']

            env_pool.append(env_count)
            total_xocc = total_xocc + occ_count
    
            x_summary = exception['EXCEPTION_SUMMARY']
            x_loc_full = x_summary['Exception Location']
            x_location = '/'+'/'.join(x_loc_full.split()[0].split('/')[-3:])
            x_line_number = x_loc_full.split()[-1]
            x_function = x_loc_full.split()[-3].replace(',','')
            installed_items = exception['INSTALLED_ITEMS']

            lines_count = 0
            triggers_count = 0
            vars_count = 0

            for item in x_traceback:
                lines_count = lines_count + len(item['RAW_CODE_SNIPPET'])
                triggers_count = triggers_count + len(item['MODULE_TRIGGERS'])
                vars_count = vars_count + len(item['MODULE_ARGS']) 
            
            count_lines = count_lines + lines_count
            count_vars  = count_vars + vars_count 
            count_triggers = count_triggers + triggers_count

            self.exceptions_tbl.add_row(
                [ 
                    colored(exception['IID'], 'green'),
                    exception['EXCEPTION_TYPE'],
                    x_function,
                    x_location,
                    x_line_number,
                    lines_count,
                    triggers_count,
                    env_count,
                    vars_count,
                    occ_count
                ]
            )    
            i_count +=1
        
        i_count = 1
        # >> load configuration issues into table 
        for issue in self.fuzz_report['CONFIGURATION']:
            self.config_issues_tbl.add_row(
                [
                    #colored('CI' + str(i_count), 'green'),
                    colored(issue['IID'], 'green'),
                    issue['STATUS'],
                    issue['METHOD'],
                    issue['ISSUE']
                ]
            )
            i_count +=1 
            
        ########################
        ########################
        ## DMT PROMPT REPORT  ##
        ########################
        ########################
        ''' s4dhu notes: I am already drafting some alternatives for reporting and presenting results 
        for the next versions (or next commits), however, this presentation via terminal 
        will always exist, it is the standard way of summarizing the results. '''

        print("\033c", end="")
        vmnf_banners.audit_report_banner('DMT')

        ### Abudct analysis ###
        cprint("\n⣆⣇      Scan settings                          \n", "white", "on_red", attrs=['bold'])        
        cprint("\tGeneral settings and siddhis called during analysis.\n",
                'cyan', attrs=[]
        )
        
        hl_color = 'green'
        sg = colored('→', hl_color, attrs=['bold'])
        
        pass_flags = ['patterns_table', 'patterns_views', 'fuzz_settings',
            'meta','download_timeout','method','headers','cookie']

        for _abd_k, _abd_v in (self.vmnf_handler.items()):
            if _abd_v and _abd_k not in pass_flags:
                if isinstance(_abd_v,(list,dict)):
                    _abd_v = len(_abd_v)

                print('{}{}:\t   {}'.format(
                    (' ' * int(5-len(_abd_k) + 15)), 
                    _abd_k, 
                    colored(_abd_v, hl_color)
                    )
                )
        print()
        sleep(1)

        ###########################
        ### target environment ####
        ###########################
        cprint("\n⣠⣾      Target Environment              ", "white", "on_red", attrs=['bold'])        
        print()
        cprint("\tDetails about target application environment.\n",
                'cyan', attrs=[]
        )

        for k,v in self.contexts['server'].items():
            k = (k.replace('_',' ')).capitalize()
            print('{}{}:\t   {}'.format(
                (' ' * int(5-len(k) + 15)),
                k,colored(v, hl_color))
            )
            sleep(0.10)

        try:
            self.contexts['environment']['EXCEPTION_REPORTER'] = \
                self.contexts['environment'].pop('DEFAULT_EXCEPTION_REPORTER_FILTER')
        except KeyError:
            self.contexts['environment']['EXCEPTION_REPORTER'] = '?'

        try:
            self.contexts['environment']['DJANGO_SETTINGS'] = \
                self.contexts['environment'].pop('DJANGO_SETTINGS_MODULE')\
                if 'DJANGO_SETTINGS_MODULE' in self.contexts['environment'] \
                    else self.contexts['environment'].pop('SETTINGS_MODULE') 
        except KeyError:
            self.contexts['environment']['DJANGO_SETTINGS'] = '?'

        for k,v in self.contexts['environment'].items():
            k = (k.replace('_',' ')).capitalize()

            print('{}{}:\t   {}'.format(
                (' ' * int(5-len(k) + 15)),
                k,colored(v, hl_color))
            )
            sleep(0.10)

        print()
        sleep(0.20)

        ##########################
        ### env leak contexts ####
        ##########################
        cprint("\n⣛⣓\tEnvLeak Contexts              ", "white", "on_red", attrs=['bold'])        
        print()
        cprint("\tEnvironment variables leaked by context.\n",
                'cyan', attrs=[]
        )
        print(self.envleak_tbl)

        ##########################
        ### Application Issues ###
        ##########################
        cprint("\n⡯⠥\tApplication Issues                ", "white", "on_red", attrs=['bold'])        
        print()
        cprint("\tSecurity weaknesses identified during {} analysis.\n".format(
                self.vmnf_handler['module_run']),
                'cyan', attrs=[]
        )
        
        for k,v in self.issues_overview.items():
            k = (k.replace('_',' ')).capitalize()
            print('{}{}:\t   {}'.format(
                (' ' * int(5-len(k) + 15)),
                k,
                colored(v, hl_color)
                )
            )
        sleep(1)

        ###################
        ### URL patterns ##
        ###################
        if self.raw_patterns:
            cprint('\nWere identified {} URL patterns that served as initial scope for fuzzing step\n'.format(
                len(self.raw_patterns)),'cyan')
            
            # mapped URL patterns (reusing dmt construted table here)
            for pattern in self.raw_patterns:
                print('   + {}'.format(pattern))
                sleep(0.05)
        
        ##################
        ### exceptions ###
        ##################
        cprint('\nWere triggered {} exceptions that lead to CWE-215 allowing information exposure'.format(
            len(self.fuzz_report['EXCEPTIONS'])),'cyan')
        
        print(self.exceptions_tbl)
        
        # get external issues references
        DJUtils().get_cwe_references()
        
        ############################
        ### configuration issues ###
        ############################
        if self.fuzz_report['CONFIGURATION']: 
            status = ('\nWere identified {} configuration issues that make it possible to infer configurations and identify technologies.'.format(
                len(self.fuzz_report['CONFIGURATION'])
                )
            )
            cprint(status, 'cyan', attrs=[])
            print(self.config_issues_tbl)
            
        ################################
        ### Framework version issues ###
        ################################
        cprint("\n⣾\tFramework Issues                  ", "white", "on_red", attrs=['bold'])        
        print()
        cprint("\tSecurity tickets and CVEs associated with the Framework version\n",'cyan', attrs=[])
        
        # Security Tickets
        cprint(']]- Security Tickets ({})'.format(tickets_siddhi), 'magenta')
        if security_tickets:
            print(self.tickets_tbl)
            print()
        else:
            print('No security tickets identified for Django {}'.format(django_version))

        # CVE IDs
        if cves:
            cprint(']]- CVE IDs ({})'.format(cve_siddhi), 'magenta')
            print(self.cves_tbl)

        report_tables = {
            'summary': self.summary_tbl,
            'tickets': self.tickets_tbl,
            'cves': self.cves_tbl,
            'exceptions': self.exceptions_tbl,
            'configuration': self.config_issues_tbl,
            'contexts': self.envleak_tbl,
            'raw_patterns': self.raw_patterns,
            'objects': self.traceback_objects_tbl

        }

        # + security_tickets: collected security tickets [list of dicts]
        self.fuzz_report['_count_issues_'] = {
            'total_lines': str(count_lines),
            'total_vars': str(count_vars),
            'total_triggers': str(count_triggers),
            'total_exceptions': str(total_xocc),
            'total_env': str(max(env_pool))
        } 
        
        vmnfshell(
            self.siddhi,
            self.fuzz_report,
            security_tickets,
            cves,
            **report_tables
        )

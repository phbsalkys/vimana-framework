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


from res.vmnf_banners import mdtt1,case_header,vmn05,create_status
from res.vmnf_validators import check_file
from neotermcolor import colored,cprint
from core.load_settings import _cs_
from datetime import datetime
import sys,os,yaml,glob
from time import sleep


class CasManager:
    def __init__(self, search_case, handler):
        self.handler = handler
        self.search_case = search_case
        self.case_files = self.get_cases()

    def handler_no_case(self):
        print("\033c", end="")
        mdtt1('white','bold')
        cprint(_cs_.get('empty_msg').format(
            '!'#datetime.now()
            ), 'cyan'
        )
        print()
        sys.exit(1)

    def flush_cases(self):
        if len(self.case_files) == 0:
            self.handler_no_case()
        
        vmn05()
        for file in os.scandir(_cs_['cases_path']):
            fmsg = ('          \t- flushing {}'.format(
                colored(file.name.split('_')[-1].split('.')[0], 'red')
                )
            )
            print(fmsg.ljust(os.get_terminal_size().columns - 1), end="\r")
            sleep(0.10)
            os.remove(file.path)
        
        smsg = colored('          \t* {} cases flushed'.format(
            len(self.case_files)), 'green')

        print(smsg.ljust(os.get_terminal_size().columns - 1), end="\r")
        print('\n\n\n')

        return 

    def update_handler(self,case_file):
        with open(case_file) as file:
            case_set = yaml.load(
                file, Loader=yaml.FullLoader
            )

            try:
                vars(self.handler).update(case_set)
            except TypeError:
                return False

        return self.handler

    def load_case(self):
        ccount = 0
        for entry in self.case_files:
            ccount +=1
            cs_id = '@cf' + str(ccount)
            
            if self.search_case == '!':
                return self.update_handler(
                    _cs_['cases_path'] + self.get_last_case()
                )

            if entry.endswith(self.search_case)\
                or self.search_case == cs_id :
                
                rel_handler = self.update_handler(_cs_['cases_path'] + entry)
                if not rel_handler:
                    print('\n[run]→ Malformed file: {}. Check it out and try again.\n'.format(
                        entry
                        )
                    )
                    sys.exit(1)

                return rel_handler

        self.list_cases()

    def get_cases(self):
        with os.scandir(_cs_['cases_path']) as saved_cases:
            return [entry.name \
                for entry in saved_cases \
                    if entry.is_file()
            ]

    def get_last_case(self):
        try:
            lentry = max(
                glob.iglob(_cs_['cases_yf']),
                    key=os.path.getctime
            )
        except ValueError:
            self.handler_no_case()

        return lentry.split('/')[-1]
        
    def list_cases(self):
        lcase = self.get_last_case()
        print("\033c", end="")
        case_header()
        cprint("\n→ Available cases:\n",'cyan')

        print('{:>19}{:>25}{:>35}{:>49}\n'.format(
            colored('id','white',attrs=['bold']),
            colored('plugin','white',attrs=['bold']),
            colored('date','white',attrs=['bold']),
            colored('case','white',attrs=['bold'])
            )
        )

        ccount = 0
        for entry in self.case_files:
            ccount +=1
            c_index = '@cf' + str(ccount)

            r_entry = entry.split('_')
            module = r_entry[0]
            date = r_entry[1]
            time = r_entry[2].split('.')[0].strip()
            exec_time = date + ' ' + time
            file_name = '_'.join(r_entry[3:]).split('.')[0]

            if entry == lcase:
                msg = ('{:>6}{:>11}{:>31}{:>31}'.format(
                    c_index,module,exec_time,file_name)
                )

                cprint(msg, 'white', 'on_green',attrs=['bold'])
                continue

            print('{:>15}{:>20}{:>40}{:>40}'.format(
                colored(c_index,'green'),
                colored(module,'green'),
                colored(exec_time, 'cyan'),
                colored(file_name, 'blue'))
            )

        print()
        sys.exit(1)

    def save_case(self):

        if self.handler['save_case'].endswith('.yaml'):
            self.handler['save_case'] = self.handler['save_case'].replace('.yaml','')
        
        case_name = self.handler['save_case']
        exec_time = str(datetime.now()).replace(' ','_') + '_'
        file_name = str(self.handler['module_run']) + '_'\
            + exec_time + self.handler['save_case'] + '.yaml'

        file_path = _cs_['cases_path'] + file_name
        self.handler['save_case'] = False

        with open(file_path, 'w') as file:
            yaml.dump(
                self.handler,
                file,
                default_flow_style=False
            )
            
        if not check_file(file_path,True):
            print("\n Error while creating case!")
            sys.exit(1)

        create_status(case_name)
        
        ''' optionally cases can be executed during creation: 
            --exec-case '''
        if not self.handler['exec_case']:
            sys.exit(0)

    def get_exec_case(self,argv):
        exec_case = str(argv[2]) + '.yaml'\
            if not str(argv[2]).endswith('.yaml') \
            and not str(argv[2]).startswith(('@cf','!'),0)\
            else str(argv[2])

        return exec_case



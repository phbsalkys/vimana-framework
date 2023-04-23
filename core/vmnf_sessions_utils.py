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

from res.vmnf_banners import case_header,mdtt1,vmn05
from pygments.formatters import TerminalFormatter
from neotermcolor import cprint, colored as cl
from pygments.lexers import PythonLexer
from pygments import highlight
from random import choice
from time import sleep



def abduct_items(**vfres):
    lights = [
        '││├˖┤', '│|│|│',
        ' |│|│', '└┐┌┘│',
        '││˖│ ', '│˖│.│',
        '├˖├˖┤'
    ]

    c,obj = False,False

    if 'guide' in (vfres):

        siddhi = vfres.get('name')
        brief  = vfres.get('brief')
        info   = vfres.get('info')

        vfres= {}
        vfres = {
            'siddhi': siddhi,
            siddhi:  brief
        }

        print(f"\t ⠞⠓⠊⠎ Abducting {cl(siddhi.lower(), 'red', attrs=['bold'])}: {cl(brief,'white')} ...")
        sleep(0.15)

    for k,v in vfres.items():
        print("\033c", end="")
        vmn05()

        _r_ = 15
        _l_ = True

        if isinstance(v,dict):
            _r_ = 4
        elif isinstance(v,list):
            _r_ = 6
        elif isinstance(v,tuple):
            _r_ = 5
        elif isinstance(v,str):
            _l_ = False
            _r_ = 2
        elif isinstance(v,int):
            _l_ = False
            _r_ = 7
        else:
            _l_ = False

        [cprint(f'{choice(lights):>24}', 'green', attrs=['blink','bold'])\
            for _ in range(_r_)
            ]

        if not _l_:
            print('\n\t\t' + highlight(str(k) + ' -|- ' +  str(v)[:500],PythonLexer(),TerminalFormatter()).strip())
            sleep(0.05)
            continue
        
        cprint(f"\n\t\t{str(k).lower()} ↓↓↓\n", 'red')

        try:
            for c,obj in enumerate(v[:20]):
                print('\t\t → ' + highlight(
                    str(obj),
                    PythonLexer(),
                    TerminalFormatter()).strip()
                )
                sleep(0.01)
            sleep(0.07)
        except TypeError:
            pass

    print("\033c", end="")
    vmn05()
    print('\n\n')

    return f'<abddone={c}:{obj}>'
    


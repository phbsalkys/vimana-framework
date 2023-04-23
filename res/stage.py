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

import yaml
import res.vmnf_validators as val

class stager:
    def __init__(self,**session):
        self.session = session
        self.stage = 'siddhis/stage.yaml'

    def forward_session(self):
        with open(self.stage, 'w') as file:
            yaml.dump(self.session, 
                file,default_flow_style=False)

    def check_forward(self,quiet:False):
        if not val.check_file(self.stage, quiet):
            return False
        
        with open(self.stage) as file:
            sts = yaml.load(file, 
                Loader=yaml.FullLoader)
        return sts

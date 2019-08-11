#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from core.compatible import generate_token
import os
import json
from database.connector import insert_honeypot_events_from_module_processor,\
    insert_honeypot_events_data_from_module_processor

class ModuleProcessor:
    """
    this is the processor to run after docker machine is up to grab the log files or do other needed process...
    """
    def __init__(self):
        self.log_filename = 'tmp/access.log'
        self.log_filename_dump = 'tmp/ohp_http_strong_password_creds_logs.json'
        self.kill_flag = False

    def processor(self):
        """
        processor function will be called as a new thread and will be die when kill_flag is True
        :return:
        """
        while not self.kill_flag:
            if os.path.exists(self.log_filename) and os.path.getsize(self.log_filename) > 0:
                # os.rename(self.log_filename, self.log_filename_dump)
                data_dump = open(self.log_filename).readlines()
+               open(self.log_filename, 'w').write('')
                # data_dump = open(self.log_filename_dump).readlines()
                for data in data_dump:
                    print(data[:-1]) # remove \n from json
            time.sleep(0.1)


def module_configuration():
    """
    module configuration

    Returns:
        JSON/Dict module configuration
    """
    return {
        "username": "admin",
        "password": generate_token(16),
        "extra_docker_options": [],
        "extra_docker_options": ["--volume {0}/tmp:/var/log/apache2/".format(os.getcwd())],
        "module_processor": ModuleProcessor()
    }

# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2023-04-10 14:34:58
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2023-04-10 22:48:45
from aux import startup
import logging
import sys

load_envs_result = startup.load_envs()
if not load_envs_result[0]:
    logging.error(load_envs_result[1])
    sys.exit(1)
    
# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2023-04-10 16:36:53
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2023-04-10 16:49:25
from aux import constants as Constants
import os
import logging 
def load_envs():
    logging.info("Loading Envs...")
    # Load Variables
    Constants.APP_ENV = os.getenv('APP_ENV', "Production")
    Constants.DB_LOCATION = os.getenv('DB_LOCATION')
    Constants.DB_NAME = os.getenv("DB_NAME")
    Constants.DB_USER = os.getenv("DB_USER")
    Constants.DB_PASSWORD = os.getenv("DB_PASSWORD")

    if Constants.APP_ENV.upper() == "PRODUCTION" and None in [
        Constants.DB_LOCATION,
        Constants.DB_NAME,
        Constants.DB_USER,
        Constants.DB_PASSWORD]:
        return False, "No database environment variables for defined. When "\
            "running in production, you should specify the database "\
            "environment variables"
    return True, ""
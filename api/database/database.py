# @Author: Rafael Direito
# @Date:   2022-10-05 16:34:49 (WEST)
# @Email:  rdireito@av.it.pt
# @Copyright: Insituto de Telecomunicações - Aveiro, Aveiro, Portugal
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2023-04-11 10:35:27

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from aux import constants as Constants
import logging
import time
import sys
import os

# Dummy database
engine = create_engine("sqlite:///./sql_app.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Only run this code when not testing
if Constants.APP_ENV != 'test':
    for i in range(10):
        try:
            # For debug!
            # IT MUST NOT BE PUT INTO PROUCTION
            logging.info(f"Trying to connect to the DB - postgresql://{Constants.DB_USER}:{Constants.DB_PASSWORD}@{Constants.DB_LOCATION}/{Constants.DB_NAME}")
            SQLALCHEMY_DATABASE_URL = f"postgresql://{Constants.DB_USER}:{Constants.DB_PASSWORD}@{Constants.DB_LOCATION}/{Constants.DB_NAME}"
            engine = create_engine(
                SQLALCHEMY_DATABASE_URL
            )
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            Base = declarative_base()
            break
        except Exception as e:
            logging.error("Waiting for DB. Will sleep 10 more seconds..." +
                          f"Exception: {e}")
            time.sleep(10)
    else:
        logging.critical("Unable to connect to database.")
        sys.exit(2)
        




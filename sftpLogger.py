import logging
import os
def logme(log_message:str,log_type:str='info',log_location='logs'):
    if not os.path.isdir("logs"): os.mkdir(log_location)
    err_log=os.path.join("logs","error.log")
    info_log=os.path.join("logs","logs.log")
    if log_type=="error":
        logging.basicConfig(filename=err_log, level=logging.ERROR,
                    format="%(asctime)s %(message)s", filemode="a+")
        logging.error(log_message)
    else:
        logging.basicConfig(filename=info_log, level=logging.DEBUG,
                        format="%(asctime)s %(message)s", filemode="a+")
        logging.info(log_message)
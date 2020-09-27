import logging
import time

logging.basicConfig(filename='example.log',level=logging.DEBUG)# 可选filemode='w')
while True:
    logging.debug('This message should go to the log file')
    logging.info('So should this')
    logging.warning('And this, too')
    time.sleep(1)
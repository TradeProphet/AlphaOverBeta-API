import logging

from AOB_API import *

if __name__ == '__main__':
    try:
        # use this email to signup, receive key , secret pair
        status_code = signup(email='portfolio4planner@gmail.com')
        status_code = signup(email='home@network.com')
    except Exception as e:
        logging.exception(str(e))
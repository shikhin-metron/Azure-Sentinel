import datetime
import logging
#import pickle
from . import DS_poller
import azure.functions as func
import os

account_id = os.environ['digitalshadowsAccountID']
customer_id = os.environ['WorkspaceID']
shared_key = os.environ['WorkspaceKey']
key = os.environ['digitalshadowsKey']
secret = os.environ['digitalshadowsSecret']

max_time = datetime.datetime.strptime("2021-09-01 05:23:25", "%Y-%m-%d %H:%M:%S")

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    
    DSobj = DS_poller.poller(account_id, key, secret, customer_id, shared_key)

    DSobj.poll()
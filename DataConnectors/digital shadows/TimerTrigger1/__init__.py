import datetime
import logging
#import pickle
from . import DS_poller
import azure.functions as func
import os

account_id = os.environ['digitalshadowsAccountID']
customer_id = os.environ['workspaceID']
shared_key = os.environ['workspaceKey']
key = os.environ['digitalshadowsKey']
secret = os.environ['digitalshadowsSecret']
connection_string = os.environ['AzureWebJobsStorage']

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    
    DSobj = DS_poller.poller(account_id, key, secret, customer_id, shared_key, connection_string)

    DSobj.poll()
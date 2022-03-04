import datetime
import logging

from . import DS_poller
import azure.functions as func
import os

account_id = os.environ['ID']
customer_id = os.environ['WID']
shared_key = os.environ['WKEY']
key = os.environ['KEY']
secret = os.environ['SECRET']
connection_string = os.environ['STORE']
historical_days = 10
url = os.environ['LIVEURI']


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    
    DSobj = DS_poller.poller(account_id, key, secret, customer_id, shared_key, connection_string, historical_days, url)
    
    DSobj.poll()
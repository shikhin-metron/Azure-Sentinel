import datetime
import logging

from . import DS_poller
import azure.functions as func
import os

logger = logging.getLogger("__init__")

account_id = os.environ['DigitalShadowsAccountID']
customer_id = os.environ['WorkspaceID']
shared_key = os.environ['WorkspaceKey']
key = os.environ['DigitalShadowsKey']
secret = os.environ['DigitalShadowsSecret']
connection_string = os.environ['AzureWebJobsStorage']
historical_days = os.environ['HistoricalDays']
url = os.environ['DigitalShadowsURL']
app = os.environ['Function']
include = os.environ['Include']
exclude = os.environ['Exclude']


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    
    DSobj = DS_poller.poller(account_id, key, secret, customer_id, shared_key, connection_string, historical_days, url)
    incList = include.split(",")
    excList = exclude.split(",")

    DSobj.poll(app, incList, excList)
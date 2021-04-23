import boto3
import time

no_of_days = 2
no_of_days_in_millis = no_of_days*86400000
token = ''
def get_log_events(log_group):
    """List the first 10000 log events from a CloudWatch group.

    :param log_group: Name of the CloudWatch log group.

    """
    global token
    file = open("todayLogs.txt","a+")
    client = boto3.client('logs')
    if token == '':
        resp = client.filter_log_events(logGroupName=log_group,logStreamNames=['access'],startTime=int(round(time.time() * 1000))-no_of_days_in_millis)
    else:
        resp = client.filter_log_events(logGroupName=log_group,logStreamNames=['access'],startTime=int(round(time.time() * 1000))-no_of_days_in_millis,nextToken=token)
    for event in resp['events']:
        file.write(event['message'].rstrip()+"\n")
    file.close()
    if "nextToken" in resp:
        token = resp['nextToken']
        get_log_events('video-production-ruby')
    else:
        token = ""

if __name__ == '__main__':
    get_log_events('video-production-ruby')


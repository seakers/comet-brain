import os
import asyncio
import aioboto3
from botocore.client import Config




################
### AIOBOTO3 ###
################


async def call_boto3_client_async(client_type, func_name, params=None, debug=True):
    if debug is True:
        print('--> ATTEMPTING ASYNC AWS CALL:', client_type, func_name)
    result = None
    session = aioboto3.Session()
    async with session.client(client_type, region_name='us-east-2', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                              aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']) as client:
        try:
            func = getattr(client, func_name)
            if params is None:
                result = await func()
            else:
                result = await func(**params)
        except Exception as ex:
            print('--> (AWS ERROR)', client_type, func_name, '-----', ex)
            return None
    return result


async def call_boto3_client_async_timeout(client_type, func_name, params=None, debug=True, connect_timeout=3):
    if debug is True:
        print('--> ATTEMPTING ASYNC AWS CALL:', client_type, func_name)
    result = None
    config = Config(connect_timeout=connect_timeout, retries={'max_attempts': 0})
    session = aioboto3.Session()
    async with session.client(client_type, region_name='us-east-2', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                              aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'], config=config) as client:
        try:
            func = getattr(client, func_name)
            if params is None:
                result = await func()
            else:
                result = await func(**params)
        except Exception as ex:
            print('--> (AWS ERROR)', client_type, func_name, '-----', ex)
            return None
    return result

async def backoff_boto3_client_async(client_type, func_name, params=None, debug=False, seconds=30):
    result = await call_boto3_client_async(client_type, func_name, params, debug)
    trys = 1
    sleep_time = 2
    attempts = int(seconds / sleep_time)
    while result is None and trys < attempts:
        result = await call_boto3_client_async(client_type, func_name, params, debug)
        trys += 1
    return 0



##############
### SEARCH ###
##############

async def find_obj(objs, key_name, key_value):
    for obj in objs:
        if key_name not in obj:
            continue
        if obj[key_name] == key_value:
            return obj
    return None


async def find_obj_value(objs, key_name, key_value, set_name):
    obj = await find_obj(objs, key_name, key_value)
    if set_name not in obj:
        return None
    return obj[set_name]


async def find_obj_and_set(objs, key_name, key_value, set_name, set_value):
    obj = await find_obj(objs, key_name, key_value)
    if obj is not None:
        obj[set_name] = set_value
    return obj


#######################
### REQUEST BACKOFF ###
#######################

async def _linear_sleep_async(x):
    await asyncio.sleep(x)










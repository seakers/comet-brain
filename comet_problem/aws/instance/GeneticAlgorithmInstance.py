from comet_problem.aws.clients.SqsClient import SqsClient
from comet_problem.aws.instance.AbstractInstance import AbstractInstance



class GeneticAlgorithmInstance(AbstractInstance):

    def __init__(self, user_info, instance=None, instance_status_info=None, instance_ssm_info=None):
        super().__init__(user_info, instance, instance_status_info, instance_ssm_info)
        self.instance_type = 'comet-algorithm'


    async def initialize(self):
        if self.instance is not None:
            await self._existing_instance()
        else:
            await self._new_resources()
            await self._new_instance(await self._definition)

    ##################
    ### PROPERTIES ###
    ##################

    @property
    async def _user_data(self):
        return '''#!/bin/bash
        . /home/ec2-user/update.sh'''

    @property
    async def _tags(self):
        return [
            {
                'Key': 'Name',
                'Value': 'comet-stack'
            },
            {
                'Key': 'ResourceGroup',
                'Value': 'comet-stack'
            },
            {
                'Key': 'IDENTIFIER',
                'Value': self.identifier
            },
            {
                'Key': 'USER_ID',
                'Value': str(self.user_id)
            },
            {
                'Key': 'RESOURCE_TYPE',
                'Value': 'comet-algorithm'
            },
            {
                'Key': 'DEPLOYMENT_TYPE',
                'Value': 'AWS'
            },
            {
                'Key': 'APOLLO_URL',
                'Value': 'http://graphql.comet:8080/v1/graphql'
            },
            {
                'Key': 'APOLLO_URL_WS',
                'Value': 'ws://graphql.comet:8080/v1/graphql'
            },
            {
                'Key': 'EVAL_REQUEST_URL',
                'Value': self.user_info.design_evaluator_request_queue_url
            },
            {
                'Key': 'EVAL_RESPONSE_URL',
                'Value': self.user_info.design_evaluator_response_queue_url
            },
            {
                'Key': 'PING_REQUEST_URL',
                'Value': self.ping_request_url
            },
            {
                'Key': 'PING_RESPONSE_URL',
                'Value': self.ping_response_url
            },
            {
                'Key': 'PRIVATE_REQUEST_URL',
                'Value': self.private_request_url
            },
            {
                'Key': 'PRIVATE_RESPONSE_URL',
                'Value': self.private_response_url
            },
            {
                'Key': 'RESOURCE_STATE',
                'Value': 'INITIALIZING'
            },
            {
                'Key': 'MESSAGE_RETRIEVAL_SIZE',
                'Value': '3'
            },
            {
                'Key': 'MESSAGE_QUERY_TIMEOUT',
                'Value': '5'
            },
            {
                'Key': 'DEBUG',
                'Value': 'false'
            }
        ]

    @property
    async def _definition(self):
        return {
            "ImageId": "ami-070051842d02c244d",  # CometServiceProdImagev3.0
            "InstanceType": "t2.small",
            "MaxCount": 1,
            "MinCount": 1,
            "SecurityGroupIds": [
                "sg-03ac54d2600b20d4c"
            ],
            "KeyName": 'gabe-master',
            "SubnetId": "subnet-08ae3e153dafe5362",
            "IamInstanceProfile": {
                'Name': 'ecsInstanceRole'
            },
            "HibernationOptions": {
                "Configured": True
            },
            "UserData": (await self._user_data),
            "TagSpecifications": [
                {
                    'ResourceType': 'instance',
                    'Tags': (await self._tags)
                },
            ],
        }


    ############
    ### PING ###
    ############

    async def ping(self):
        response = dict()
        response['instance'] = await self._ping_instance()
        response['container'] = await self._ping_container()
        response['init_status'] = await self.get_tag('RESOURCE_STATE')
        response['PING_REQUEST_QUEUE'] = self.ping_request_url
        response['PING_RESPONSE_QUEUE'] = self.ping_response_url
        response['PRIVATE_REQUEST_QUEUE'] = self.private_request_url
        response['PRIVATE_RESPONSE_QUEUE'] = self.private_response_url
        return response

    async def _ping_container(self):
        info = {
            'Status': None
        }
        if await self.get_instance_ssm_status() == 'Online' and await self.container_running():
            info['Status'] = 'Running'
        else:
            info['Status'] = 'Stopped'
        return info



    ################
    ### CONSOLE  ###
    ################

    async def start_ga(self):

        # --> 1. Check container running
        if await self.get_instance_state() != 'running' or not await self.container_running():
            return False

        # --> 2. Send start msg
        response = await SqsClient.send_start_ga_msg(self.private_request_url,
                                                     self.eosscontext.group_id,
                                                     self.eosscontext.problem_id,
                                                     self.eosscontext.dataset_id,
                                                     self.private_response_url)
        return response is not None

    async def stop_ga(self):

        # --> 1. Check container running
        if await self.get_instance_state() != 'running' or not await self.container_running():
            return False

        # --> 2. Send start msg
        response = await SqsClient.send_stop_ga_msg(self.private_request_url, self.private_response_url)
        return response is not None

    async def apply_feature(self):
        return 0














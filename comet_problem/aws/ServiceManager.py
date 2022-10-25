import asyncio
import json

from comet_auth.helpers import save_user_info_async
from comet_auth.models import UserInformation
from comet_problem.aws.clients.SqsClient import SqsClient
from comet_problem.aws.instance.InstanceManager import InstanceManager



class ServiceManager:
    
    
    
    def __init__(self, user_info: UserInformation):
        self.user_info = user_info
        self.user_id = user_info.id

        # --> Instance Managers
        self.de_manager = InstanceManager(self.user_info, 'comet-evaluator')
        self.ga_manager = InstanceManager(self.user_info, 'comet-algorithm')
        
        
        
    async def initialize(self, blocking=True):

        # --> 1. Create user resources (queues, etc...)
        save = False
        if self.user_info.design_evaluator_request_queue_name is None:
            queue_name = 'user-' + str(self.user_id) + '-comet-evaluator-request-queue'
            self.user_info.design_evaluator_request_queue_name = queue_name
            self.user_info.design_evaluator_request_queue_url = await SqsClient.create_queue_name(queue_name)
            save = True
        if self.user_info.design_evaluator_response_queue_name is None:
            queue_name = 'user-' + str(self.user_id) + '-comet-evaluator-response-queue'
            self.user_info.design_evaluator_response_queue_name = queue_name
            self.user_info.design_evaluator_response_queue_url = await SqsClient.create_queue_name(queue_name)
            save = True
        if save:
            await save_user_info_async(self.user_info)

        # --> 2. Initialize Managers
        async_tasks = []
        async_tasks.append(asyncio.create_task(self.de_manager.initialize()))
        async_tasks.append(asyncio.create_task(self.ga_manager.initialize()))
        if blocking:
            for task in async_tasks:
                await task
        return True


    async def gather(self, blocking=True):

        # --> 1. Gather Managers
        async_tasks = []
        async_tasks.append(asyncio.create_task(self.de_manager.gather()))
        async_tasks.append(asyncio.create_task(self.ga_manager.gather()))
        if blocking:
            for task in async_tasks:
                await task
        return True

    ############
    ### PING ###
    ############


    async def ping_services(self):

        async def add_to_survey(instance_manager, internal_survey, key):
            ping_result = await instance_manager.ping_instances()
            internal_survey[key] = ping_result

        survey = {
            'comet-evaluator': [],
            'comet-algorithm': []
        }
        async_tasks = []
        async_tasks.append(asyncio.create_task(add_to_survey(self.de_manager, survey, 'comet-evaluator')))
        async_tasks.append(asyncio.create_task(add_to_survey(self.ga_manager, survey, 'comet-algorithm')))
        for task in async_tasks:
            await task

        return survey

    #####################
    ### CONTROL PANEL ###
    #####################

    async def resource_msg(self, instance_ids, command, blocking=False):
        results = {
            'comet-evaluator': [],
            'comet-algorithm': []
        }
        async_tasks = []
        async_tasks.append(
            asyncio.create_task(
                self._resource_msg(self.de_manager, instance_ids['comet-evaluator'], command, results, 'comet-evaluator')
            )
        )
        async_tasks.append(
            asyncio.create_task(
                self._resource_msg(self.ga_manager, instance_ids['comet-algorithm'], command, results, 'comet-algorithm')
            )
        )
        if blocking is False:
            return {}
        for task in async_tasks:
            await task
        return results

    async def _resource_msg(self, manager, instance_ids, command, results, key):
        result = await manager.resource_msg(instance_ids, command, blocking=True)
        results[key] = result

    ############
    ### LOCK ###
    ############

    @property
    async def lock(self):
        return self.user_info.service_lock

    async def lock_services(self):
        self.user_info.service_lock = True
        await save_user_info_async(self.user_info)

    async def unlock_services(self):
        self.user_info.service_lock = False
        await save_user_info_async(self.user_info)













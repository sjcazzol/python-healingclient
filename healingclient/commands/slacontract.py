# -*- coding: utf-8 -*-
#
# Copyright 2014 - Intel
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#

from cliff.command import Command as BaseCommand
from cliff.lister import Lister as ListCommand
from cliff.show import ShowOne as ShowCommand

from healingclient.openstack.common import log as logging
from healingclient.api.slacontract import SLAContractManager

LOG = logging.getLogger(__name__)


def format(slacontract=None):
    columns = (
        'ID',
        'Project_ID',
        'Type',
        'Value',
        'Action',
        'Action Options',
        'Resource_ID'
    )

    if slacontract:
        data = (
            slacontract.id,
            slacontract.name or '<none>',
            slacontract.project_id or '<none>',
            slacontract.type,
            slacontract.value or '<none>',
            slacontract.action,
            slacontract.action_options,
            slacontract.resource_id or '<none>'
        )
    else:
        data = []

    return columns, data


class List(ListCommand):
    "List all slacontracts"

    def take_action(self, parsed_args):
        data = [format(slacontract)[1] for slacontract
                in SLAContractManager(self.app.client).list()]

        if data:
            return (format()[0], data)
        else:
            return format()


class Get(ShowCommand):
    "Show a specific slacontract"

    def get_parser(self, prog_name):
        parser = super(Get, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            help='ID')
        return parser

    def take_action(self, parsed_args):
        slacontract = SLAContractManager(self.app.client).get(parsed_args.id)

        return format(slacontract)


class Create(ShowCommand):
    "Create new slacontract"

    def get_parser(self, prog_name):
        parser = super(Create, self).get_parser(prog_name)
        parser.add_argument(
            '-project_id',
            help='Project ID')
        parser.add_argument(
            '-name',
            help='Contract Name')
        parser.add_argument(
            'type',
            choices=['HOST_DOWN', 'VM_ERROR', 'RESOURCE',
                     'CEILOMETER_EXTERNAL_RESOURCE', 'GENERIC_SCRIPT_ALARM',
                     'NOTIFICATION_ALARM'],
            help='Contract Type')
        parser.add_argument(
            'value',
            help='Contract value')
        parser.add_argument(
            'action',
            help='Action to take'
        )
        parser.add_argument(
            '-alarm_data',
            help="Alarm Data dict. '{\"period\": \"20\"}'")
        parser.add_argument(
            '-action_options',
            help="Action Specific Options dict '{\"period\": \"20\"}'")
        parser.add_argument(
            '-resource_id',
            help='Target resouce ( depends on the contract type)'
        )
        
        return parser

    def take_action(self, parsed_args):
        slacontract = SLAContractManager(self.app.client)\
            .create(parsed_args.project_id,
                    parsed_args.type,
                    parsed_args.value,
                    parsed_args.action,
                    parsed_args.alarm_data,
                    parsed_args.resource_id,
                    parsed_args.action_options,
                    parsed_args.name)

        return format(slacontract)


class Delete(BaseCommand):
    "Delete a slacontract"

    def get_parser(self, prog_name):
        parser = super(Delete, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            help='ID')

        return parser

    def take_action(self, parsed_args):
        SLAContractManager(self.app.client).delete(parsed_args.id)


class Update(ShowCommand):
    "Update a slacontract"

    def get_parser(self, prog_name):
        parser = super(Update, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            help='ID')
        parser.add_argument(
            '-name',
            help='Contract Name')
        parser.add_argument(
            '-value',
            help='Contract value')
        parser.add_argument(
            '-alarm_data',
            help="Alarm Data dict. '{\"period\": \"20\"}'")
        parser.add_argument(
            '-action_options',
            help="Action Options dict. '{\"period\": \"20\"}'")
        parser.add_argument(
            '-action',
            help='Action to take'
        )
        return parser

    def take_action(self, parsed_args):
        slacontract = SLAContractManager(self.app.client)\
            .update(parsed_args.id,
                    parsed_args.value,
                    parsed_args.action,
                    parsed_args.alarm_data,
                    parsed_args.action_options,
                    parsed_args.name)

        return format(slacontract)

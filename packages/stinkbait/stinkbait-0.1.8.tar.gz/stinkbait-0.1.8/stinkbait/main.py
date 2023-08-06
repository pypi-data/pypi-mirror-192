#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import external packages
import argparse
import boto3
import sys
import os
import sys
import configparser


# Import stinkbait modules
from stinkbait.session import StinkbaitSession as session
import stinkbait.arguments as arguments
from stinkbait.logger_config import logger
#import stinkbait.orgs.orgs as orgs
#import stinkbait.orgs.campaigns as campaigns
#import stinkbait.orgs.targets as targets
#import stinkbait.playbooks.playbooks as playbooks
#import stinkbait.users.users as users

def main():
    while True:
        command_map = {
            'create': {
                'organization': 'Create Organization',
                'campaign': 'Create Campaign',
                'target': 'Create Target',
                'user': 'Create User'
            },
            'update': {
                'organization': 'Update Organization',
                'campaign': 'Update Campaign',
                'target': 'Update Target',
                'user': 'Update User'
            },
            'delete': {
                'organization': 'Delete Organization',
                'campaign': 'Delete Campaign',
                'target': 'Delete Target',
                'user': 'Delete User'
            },
            'list': {
                'organization': 'List Organization',
                'campaign': 'List Campaign',
                'target': 'List Target',
                'user': 'List User'
            },
            'run': {
                'playbook': 'Run Playbook'
            },
        }
        # parse the arguments module and return the args and parser
        session_args = arguments.args()
        args = session_args[0]
        parser = session_args[1]
        # set the stinkbait session
        stinkbait_session = session.stinkbait_session_handler(args)
        logger.info(f'StinkBait User Session Info: {stinkbait_session}')
        logger.info(f'User Provided Arguments: {args}')

        # If the command is in the command map, then execute the command
        if args.command in command_map:
            sub_command = getattr(args, f"{args.command}_command")
            if sub_command in command_map[args.command]:
                print(command_map[args.command][sub_command])
        else:
            print("No StinkBait command provided.  Please use --help for more information.")
            while True:
                new_command = input("StinkBait > ")
                try:
                    session_args = arguments.args(new_command)
                except Exception as e:
                    print(e)
                    print(parser.print_help())
                    continue
                    # sys.exit(1)
                args = session_args[0]
                parser = session_args[1]

if __name__ == '__main__':
    main(args)
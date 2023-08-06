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
import stinkbait.session as session
import stinkbait.arguments as arguments
#import stinkbait.orgs.orgs as orgs
#import stinkbait.orgs.campaigns as campaigns
#import stinkbait.orgs.targets as targets
#import stinkbait.playbooks.playbooks as playbooks
#import stinkbait.users.users as users

def main():
    args = arguments.args()
    if args is None:
        print("No StinkBait command provided.  Please use --help for more information.")
        #TODO add help menu
        sys.exit(1)
    else:
        stinkbait_session = session.stinkbait_session_handler(args)
        print(f'StinkBait User Session Info: {stinkbait_session}')
        print(f'User Provided Arguments: {args}')
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
        }
    }

    if args.command in command_map:
        sub_command = getattr(args, f"{args.command}_command")
        if sub_command in command_map[args.command]:
            print(command_map[args.command][sub_command])

        else:
            print("No StinkBait command provided.  Please use --help for more information.")
            #TODO add help menu
            sys.exit(1)

if __name__ == '__main__':
    main(args)
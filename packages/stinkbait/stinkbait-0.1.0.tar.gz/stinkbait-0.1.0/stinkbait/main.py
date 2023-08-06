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
        if args.command == 'create':
            if args.create_command == 'organization':
                org_name = args.organization
                org_owner = args.owner
                results = orgs.add_org(stinkbait_session, args)
                print(results)

                print('Create Organization')
            elif args.create_command == 'campaign':
                print('Create Campaign')
            elif args.create_command == 'target':
                print('Create Target')
            elif args.create_command == 'user':
                print('Create User')
        elif args.command == 'update':
            if args.update_command == 'organization':
                print('Update Organization')
            elif args.update_command == 'campaign':
                print('Update Campaign')
            elif args.update_command == 'target':
                print('Update Target')
            elif args.update_command == 'user':
                print('Update User')
        elif args.command == 'delete':
            if args.delete_command == 'organization':
                print('Delete Organization')
            elif args.delete_command == 'campaign':
                print('Delete Campaign')
            elif args.delete_command == 'target':
                print('Delete Target')
            elif args.delete_command == 'user':
                print('Delete User')
        elif args.command == 'list':
            if args.list_command == 'organization':
                print('List Organization')
            elif args.list_command == 'campaign':
                print('List Campaign')
            elif args.list_command == 'target':
                print('List Target')
            elif args.list_command == 'user':
                print('List User')
        elif args.command == 'run':
            if args.run_command == 'playbook':
                print('Run Playbook')
        else:
            print("No StinkBait command provided.  Please use --help for more information.")
            #TODO add help menu
            sys.exit(1)

if __name__ == '__main__':
    main(args)
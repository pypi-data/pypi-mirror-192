#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import sys

"""
Arguments for StinkBait
"""
    ########################################################################################
    #############################Begin Argument Parser######################################
def args(new_command=None):
    parser = argparse.ArgumentParser(prog='stinkbait', description='Security Awareness Testing and Training Tool', epilog='Why should red teamers have all the fun?')
    subparsers = parser.add_subparsers(dest='command')

    # Subparser for "Create"
    create_parser = subparsers.add_parser('create')
    create_subparsers = create_parser.add_subparsers(dest='create_command')

    #Subparser for "Create Organization"
    create_organization_parser = create_subparsers.add_parser('organization')
    create_organization_parser.add_argument('--profile', default='default', required=False, help='AWS profile to use for this command.  Default is "default".')
    create_organization_parser.add_argument('--region', default='us-east-1', required=False, help='AWS region to use for this command.  Default is "us-east-1".')
    create_organization_parser.add_argument('--org-name', required=True, help='Name of the organization to create.')
    create_organization_parser.add_argument('--org-owner', required=True, help='Owner of the organization to create.')


    #Subparser for "Create Campaign"
    create_campaign_parser = create_subparsers.add_parser('campaign')
    create_campaign_parser.add_argument('--profile', default='default', required=False, help='AWS profile to use for this command.  Default is "default".')
    create_campaign_parser.add_argument('--region', default='us-east-1', required=False, help='AWS region to use for this command.  Default is "us-east-1".')
    create_campaign_parser.add_argument('--org-name', required=True, help='Organization to create the campaign in.')
    create_campaign_parser.add_argument('--campaign-name', required=True, help='Campaign to create.')

    #Subparser for "Create Target"
    create_target_parser = create_subparsers.add_parser('target')
    create_target_parser.add_argument('--profile', default='default', required=False, help='AWS profile to use for this command.  Default is "default".')
    create_target_parser.add_argument('--region', default='us-east-1', required=False, help='AWS region to use for this command.  Default is "us-east-1".')
    create_target_parser.add_argument('--organization', required=True, help='Organization to create the target in.')
    create_target_parser.add_argument('--target-first-name', required=True, help='First name of the target.')
    create_target_parser.add_argument('--target-last-name', required=True, help='Last name of the target.')
    create_target_parser.add_argument('--target-email', required=False, help='Email address of the target.')
    create_target_parser.add_argument('--target-phone', required=False, help='Phone number of the target.')

    #Subparser for "Create User"
    create_user_parser = create_subparsers.add_parser('user')
    create_user_parser.add_argument('--profile', default='default', required=False, help='AWS profile to use for this command.  Default is "default".')
    create_user_parser.add_argument('--region', default='us-east-1', required=False, help='AWS region to use for this command.  Default is "us-east-1".')
    create_user_parser.add_argument('--email', required=True, help='Email address of the user to create.')
    create_user_parser.add_argument('--first-name', required=False, help='First name of the user.')
    create_user_parser.add_argument('--last-name', required=False, help='Last name of the user.')

    # Subparser for "Update"
    update_parser = subparsers.add_parser('update')
    update_subparsers = update_parser.add_subparsers(dest='update_command')
    update_organization_parser = update_subparsers.add_parser('organization')

    #Subparser for "Update Organization"
    update_organization_command_parser = update_organization_parser.add_subparsers(dest='update_organization_command')

    #Subparser for "Update Organization Add User"
    add_user_parser = update_organization_command_parser.add_parser('add_user')
    add_user_parser.add_argument('--profile', default='default', required=False, help='AWS profile to use for this command.  Default is "default".')
    add_user_parser.add_argument('--region', default='us-east-1', required=False, help='AWS region to use for this command.  Default is "us-east-1".')
    add_user_parser.add_argument('--email', required=True, help='Email address of the user to add.')

    #Subparser for "Update Organization Remove User"
    remove_user_parser = update_organization_command_parser.add_parser('remove_user')
    remove_user_parser.add_argument('--profile', default='default', required=False, help='AWS profile to use for this command.  Default is "default".')
    remove_user_parser.add_argument('--region', default='us-east-1', required=False, help='AWS region to use for this command.  Default is "us-east-1".')
    remove_user_parser.add_argument('--email', required=True, help='Email address of the user to remove.')

    #Subparser for "Update Organization Add Campaign"
    add_campaign_parser = update_organization_command_parser.add_parser('add_campaign')
    add_campaign_parser.add_argument('--profile', default='default', required=False, help='AWS profile to use for this command.  Default is "default".')
    add_campaign_parser.add_argument('--region', default='us-east-1', required=False, help='AWS region to use for this command.  Default is "us-east-1".')
    add_campaign_parser.add_argument('--campaign-name', required=True, help='Name of the campaign to add.')

    #Subparser for "Update Organization Remove Campaign"
    remove_campaign_parser = update_organization_command_parser.add_parser('remove_campaign')
    remove_campaign_parser.add_argument('--profile', default='default', required=False, help='AWS profile to use for this command.  Default is "default".')
    remove_campaign_parser.add_argument('--region', default='us-east-1', required=False, help='AWS region to use for this command.  Default is "us-east-1".')
    remove_campaign_parser.add_argument('--campaign-name', required=True, help='Name of the campaign to remove.')

    #Subparser for "Update Organization Add Target"

    #Subparser for "Update Campaign"
    update_campaign_parser = update_subparsers.add_parser('campaign')
    update_campaign_parser.add_argument('--profile', default='default', required=False, help='AWS profile to use for this command.  Default is "default".')
    update_campaign_parser.add_argument('--region', default='us-east-1', required=False, help='AWS region to use for this command.  Default is "us-east-1".')

    #Subparser for "Update Target"
    update_target_parser = update_subparsers.add_parser('target')
    update_target_parser.add_argument('--profile', default='default', required=False, help='AWS profile to use for this command.  Default is "default".')
    update_target_parser.add_argument('--region', default='us-east-1', required=False, help='AWS region to use for this command.  Default is "us-east-1".')
    
    #Subparser for "Update User"
    update_user_parser = update_subparsers.add_parser('user')
    update_user_parser.add_argument('--profile', default='default', required=False, help='AWS profile to use for this command.  Default is "default".')
    update_user_parser.add_argument('--region', default='us-east-1', required=False, help='AWS region to use for this command.  Default is "us-east-1".')
    update_user_parser.add_argument('--email', required=True, help='Email address of the user to update.')
    update_user_parser.add_argument('--first-name', required=False, help='First name of the user.')
    update_user_parser.add_argument('--last-name', required=False, help='Last name of the user.')
    update_user_parser.add_argument('--password', required=False, help='Password of the user.')
    update_user_parser.add_argument('--phone', required=False, help='Phone number of the user.')
    update_user_parser.add_argument('--github', required=False, help='Github username of the user.')
    update_user_parser.add_argument('--slack', required=False, help='Slack username of the user.')
    update_user_parser.add_argument('--discord', required=False, help='Discord username of the user.')
    update_user_parser.add_argument('--teams', required=False, help='Microsoft Teams username of the user.')

    # Subparser for "Delete"
    delete_parser = subparsers.add_parser('delete')
    delete_subparsers = delete_parser.add_subparsers(dest='delete_command')

    # Subparser for "Delete Organization"
    delete_organization_parser = delete_subparsers.add_parser('organization')
    delete_organization_parser.add_argument('--profile', default='default', required=False, help='AWS profile to use for this command.  Default is "default".')
    delete_organization_parser.add_argument('--region', default='us-east-1', required=False, help='AWS region to use for this command.  Default is "us-east-1".')
    delete_organization_parser.add_argument('--organization', required=True, help='Organization to delete.')
    delete_organization_parser.add_argument('--force', action='store_true', help='Force the deletion of the organization.')

    # Subparser for "Delete Campaign"
    delete_campaign_parser = delete_subparsers.add_parser('campaign')
    delete_campaign_parser.add_argument('--profile', default='default', required=False, help='AWS profile to use for this command.  Default is "default".')
    delete_campaign_parser.add_argument('--region', default='us-east-1', required=False, help='AWS region to use for this command.  Default is "us-east-1".')
    delete_campaign_parser.add_argument('--campaign-name', required=True, help='Campaign to delete.')
    delete_campaign_parser.add_argument('--force', action='store_true', help='Force the deletion of the campaign.')

    # Subparser for "Delete Target"
    delete_target_parser = delete_subparsers.add_parser('target')
    delete_target_parser.add_argument('--profile', default='default', required=False, help='AWS profile to use for this command.  Default is "default".')
    delete_target_parser.add_argument('--region', default='us-east-1', required=False, help='AWS region to use for this command.  Default is "us-east-1".')
    delete_target_parser.add_argument('--email', required=True, help='Email address of the target to delete.')
    delete_target_parser.add_argument('--force', action='store_true', help='Force the deletion of the target.')

    # Subparser for "Delete User"
    delete_user_parser = delete_subparsers.add_parser('user')
    delete_user_parser.add_argument('--profile', default='default', required=False, help='AWS profile to use for this command.  Default is "default".')
    delete_user_parser.add_argument('--region', default='us-east-1', required=False, help='AWS region to use for this command.  Default is "us-east-1".')
    delete_user_parser.add_argument('--email', required=True, help='Email address of the user to delete.')
    delete_user_parser.add_argument('--force', action='store_true', help='Force the deletion of the user.')

    # Subparser for "List"
    list_parser = subparsers.add_parser('list')
    list_subparsers = list_parser.add_subparsers(dest='list_command')

    # Subparser for "List Organizations"
    list_organization_parser = list_subparsers.add_parser('organization')
    list_organization_parser.add_argument('--profile', default='default', required=False, help='AWS profile to use for this command.  Default is "default".')
    list_organization_parser.add_argument('--region', default='us-east-1', required=False, help='AWS region to use for this command.  Default is "us-east-1".')

    # Subparser for "List Campaigns"
    list_campaign_parser = list_subparsers.add_parser('campaign')
    list_campaign_parser.add_argument('--profile', default='default', required=False, help='AWS profile to use for this command.  Default is "default".')
    list_campaign_parser.add_argument('--region', default='us-east-1', required=False, help='AWS region to use for this command.  Default is "us-east-1".')

    # Subparser for "List Targets"
    list_target_parser = list_subparsers.add_parser('target')
    list_target_parser.add_argument('--profile', default='default', required=False, help='AWS profile to use for this command.  Default is "default".')
    list_target_parser.add_argument('--region', default='us-east-1', required=False, help='AWS region to use for this command.  Default is "us-east-1".')

    # Subparser for "List Users"
    list_user_parser = list_subparsers.add_parser('user')
    list_user_parser.add_argument('--profile', default='default', required=False, help='AWS profile to use for this command.  Default is "default".')
    list_user_parser.add_argument('--region', default='us-east-1', required=False, help='AWS region to use for this command.  Default is "us-east-1".')
    list_user_parser.add_argument('--email', required=False, help='Email address of the user to list.')

    # Subparser for "Run Playbook"
    run_parser = subparsers.add_parser('run')
    run_subparsers = run_parser.add_subparsers(dest='run_command')

    run_playbook_parser = run_subparsers.add_parser('playbook')
    run_playbook_parser.add_argument('--profile', default='default', required=False, help='AWS profile to use for this command.  Default is "default".')
    run_playbook_parser.add_argument('--region', default='us-east-1', required=False, help='AWS region to use for this command.  Default is "us-east-1".')
    run_playbook_parser.add_argument('--provider', required=True, help="Technology Provider of the Playbook - e.g. aws, azure, gcp, etc.")
    run_playbook_parser.add_argument('--playbook-name', required=True, help="Name of the playbook to run")
    run_playbook_parser.add_argument('--organization', required=False, help="Organization associated with the playbook")
    run_playbook_parser.add_argument('--campaign', required=False, help="Campaign associated with the playbook")
    run_playbook_parser.add_argument('--provider_key', required=False, help="If your provider isn't AWS, you need to explicitly provide the key to use")

    # Subparser for "Quit"
    quit_parser = subparsers.add_parser('quit')

    # Subparser for "Help"
    help_parser = subparsers.add_parser('help')

    parser.add_argument('--profile', required=False, help='AWS profile to use')
    parser.add_argument('--region', required=False, help='AWS region to use')

    if new_command == None:
        try:
            args = parser.parse_args()
            return args, parser
        except Exception as e:
            print(e)
            return None, None
    elif new_command == 'help':
        parser.print_help()
        return None, None
    elif new_command == 'quit':
        sys.exit(0)
    else:
        try:
            args = parser.parse_args(new_command.split())
        except SystemExit:
            return None, None
#        return args, parser
    # Parse Quit and Help Commands Before Returning to Main Function 
    if args.command == 'quit':
        sys.exit(0)
    elif args.command == 'help':
        parser.print_help()
    #############################End Argument Parser########################################
    ########################################################################################
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
    logger.info('Starting StinkBait')
    while True:
        # parse the arguments module and return the args and parser
        session_args = arguments.args()
        args = session_args[0]
        parser = session_args[1]
        # Set the stinkbait session, including local user public IP and boto3 session
        stinkbait_session = session.stinkbait_session_handler(args)
        logger.debug(f'StinkBait User Session Info: {stinkbait_session}')
        logger.debug(f'User Provided Arguments: {args}')

        #TODO: Add functionality where if the user provides a command on initial execution, it's evaluated.

        # Enter an infinite loop where the user can continue to enter commands minus stinkbait keyword and it keeps executing new commands
        while True:
            new_command = input("StinkBait > ")
            if new_command == 'exit' or new_command == 'quit':
                sys.exit(0)
            elif new_command == 'help':
                parser.print_help()
            else:
                new_command = arguments.args(new_command)
                args = new_command[0]
                logger.debug(f'User Provided Arguments: {args}')

if __name__ == '__main__':
    main(args)
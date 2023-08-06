import requests as req
import configparser
from bs4 import BeautifulSoup
import boto3
import uuid
import time
from bs4 import BeautifulSoup
from stinkbait.logger_config import logger
class StinkbaitSession:
    def __init__(self, args):
        self.args = args
        self.stinkbait_session = self.stinkbait_session_handler(args)

    def stinkbait_session_handler(args=None):
        print("Initializing user session", end="")
        for i in range(3):
            print(".", end="")
            time.sleep(1)
        print("")
        #Check and store User Public IP Address
        for i in range(3):
            try:
                ip = req.get("http://checkip.dyndns.org")
                soup = BeautifulSoup(ip.text, "html.parser")
                user_ip = soup.find("body").text.split(":")[1].strip()
                break
            except:
                if i == 2:
                    logger.warning("Unable to determine user Public IP Address")
                    return None
                else:
                    logger.warning("Initial IP Address Unsuccessful, Trying Again...")
        #Initiate AWS Session
        for i in range(3):
            try:
                boto3_session = boto3.Session(profile_name=args.profile, region_name=args.region)
                break
            except:
                if i == 2:
                    logger.warning("Unable to initiate AWS Session")
                    return None
                else:
                    logger.warning("Initial AWS Session Attempt Unsuccessful, Trying Again...")   
        #Check and Store AWS Principal ARN and Account #
        sts = boto3_session.client('sts')
        caller_identity = sts.get_caller_identity()
        aws_account = caller_identity['Arn'].split(":")[4]
        aws_principal = caller_identity['Arn']
        logger.info(f'Your AWS Account: {aws_account}')
        logger.info(f'Your AWS Principal: {aws_principal}')
    ########################################################################################
    ###############################START CONFIG PARSER######################################
        #Set config.ini file configuration data to persist between sessions
        config = configparser.ConfigParser()
        config.read('config.ini')
        if not config.has_section('STINKBAIT'):
            config.add_section('STINKBAIT')

        if not config.has_option('STINKBAIT', 'stinkbait_version'):
            config.set('STINKBAIT', 'stinkbait_version', '0.1.0')

        if not config.has_section('STINKBAIT_USER'):
            config.add_section('STINKBAIT_USER')

        if not config.has_option('STINKBAIT_USER', 'stinkbait_user_ip') or config.get('STINKBAIT_USER', 'stinkbait_user_ip') == None:
            config.set('STINKBAIT_USER', 'stinkbait_user_ip', user_ip)

        if not config.has_option('STINKBAIT_USER', 'stinkbait_aws_account'):
            config.set('STINKBAIT_USER', 'stinkbait_aws_account', aws_account)

        if not config.has_option('STINKBAIT_USER', 'stinkbait_aws_principal'):
            config.set('STINKBAIT_USER', 'stinkbait_aws_principal', aws_principal)

        if config.has_option('stinkbait config', 'stinkbait_organizations_list'):
            stinkbait_organizations_list = config.get('stinkbait', 'stinkbait_organizations_list')
            logger.info(f'Your Stinkbait Organizations: {stinkbait_organizations_list}')
        else:
            stinkbait_organizations_list = None
            logger.info(f'Your Stinkbait Organizations: None')
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    ###############################END CONFIG PARSER########################################
    ########################################################################################

        #Return session data
        return boto3_session, user_ip, aws_account, aws_principal

    def console_session(args, stinkbait_session):
        print('TODO: Console Session for Users - needs role creation, add user to cloud9 environment in c2 cfn template to work properly')
        print('Provides a URL that can be used to sign in to the AWS Management Console as a federated user - i.e. red team operators.')
        import urllib, json, sys
        import requests # 'pip install requests'
        import boto3 # AWS SDK for Python (Boto3) 'pip install boto3'

        # Step 1: Authenticate user in your own identity system.

        # Step 2: Using the access keys for an IAM user in your AWS account,
        # call "AssumeRole" to get temporary access keys for the federated user

        # Note: Calls to AWS STS AssumeRole must be signed using the access key ID 
        # and secret access key of an IAM user or using existing temporary credentials.
        # The credentials can be in Amazon EC2 instance metadata, in environment variables, 
        # or in a configuration file, and will be discovered automatically by the 
        # client('sts') function. For more information, see the Python SDK docs:
        # http://boto3.readthedocs.io/en/latest/reference/services/sts.html
        # http://boto3.readthedocs.io/en/latest/reference/services/sts.html#STS.Client.assume_role
        sts_connection = boto3.client('sts')

        assumed_role_object = sts_connection.assume_role(
            RoleArn="arn:aws:iam::account-id:role/ROLE-NAME",
            RoleSessionName="AssumeRoleSession",
        )

        # Step 3: Format resulting temporary credentials into JSON
        url_credentials = {}
        url_credentials['sessionId'] = assumed_role_object.get('Credentials').get('AccessKeyId')
        url_credentials['sessionKey'] = assumed_role_object.get('Credentials').get('SecretAccessKey')
        url_credentials['sessionToken'] = assumed_role_object.get('Credentials').get('SessionToken')
        json_string_with_temp_credentials = json.dumps(url_credentials)

        # Step 4. Make request to AWS federation endpoint to get sign-in token. Construct the parameter string with
        # the sign-in action request, a 12-hour session duration, and the JSON document with temporary credentials 
        # as parameters.
        request_parameters = "?Action=getSigninToken"
        request_parameters += "&SessionDuration=43200"
        if sys.version_info[0] < 3:
            def quote_plus_function(s):
                return urllib.quote_plus(s)
        else:
            def quote_plus_function(s):
                return urllib.parse.quote_plus(s)
        request_parameters += "&Session=" + quote_plus_function(json_string_with_temp_credentials)
        request_url = "https://signin.aws.amazon.com/federation" + request_parameters
        r = requests.get(request_url)
        # Returns a JSON document with a single element named SigninToken.
        signin_token = json.loads(r.text)

        # Step 5: Create URL where users can use the sign-in token to sign in to 
        # the console. This URL must be used within 15 minutes after the
        # sign-in token was issued.
        request_parameters = "?Action=login" 
        request_parameters += "&Issuer=Example.org" 
        request_parameters += "&Destination=" + quote_plus_function("https://console.aws.amazon.com/")
        request_parameters += "&SigninToken=" + signin_token["SigninToken"]
        request_url = "https://signin.aws.amazon.com/federation" + request_parameters

        # Send final URL to stdout
        print (request_url)
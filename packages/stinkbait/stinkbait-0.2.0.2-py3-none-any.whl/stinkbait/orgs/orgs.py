#!/usr/bin/env python3
import boto3
class Targets:
    '''
    Create a Class 'Targets'.
    The class will be used to define the e-mail addresses of users to be targeted in an e-mail campaign using SES - they will be stored in a DynamoDB table called stinkbait_targets.
    Once stored, they will be included in any campaigns they are associated with, unless they are removed from the table.
    
    To initialize the class, the following parameters are required:
    stinkbait_session - the stinkbait user session object
    target_email - the e-mail address of the target
    target_org - the company of the target
    target_name - the name of the target

    and the following parameters are optional:
    target_title - the title of the target
    target_phone - the phone number of the target
    target_address - the address of the target
    target_city - the city of the target
    target_state - the state of the target
    target_zip - the zip code of the target
    target_country - the country of the target
    target_notes - any notes about the target

    We know that stinkbait_session is a complex object and we can retrieve the stinkbait_instance_id. The stinkbait_instance_id can used to call dynamodb in using a boto3 session that is also part of the stinkbait_session object. The stinkbait_instance_id is stored at [1][3] and the boto3 session is stored at [1][0]. As the first step of initialization, we need to check and see if a targets table has been created using the format {stinkbait-targets-{stinkbait_instance_id}}. 
    However, the last user session could have been in a different region. We need to get available regions via ec2 and then check each region to see if a table exists. If a table exists, we can use it. If not, we need to create it. You will need a try except loop to catch the exception if the region is not available. If the table does not exist, we need to create it using the region in the current session.

    The following methods are available:
    add_target - add a target to the stinkbait_targets table
    remove_target - remove a target from the stinkbait_targets table
    update_target - update a target in the stinkbait_targets table
    get_target - get a target from the stinkbait_targets table
    list_targets - list all targets in the stinkbait_targets table
    ChatGPT Response Below:
    '''
    def __init__(self, stinkbait_session, target_email, target_name, target_org=None, target_title=None,
                 target_phone=None, target_address=None, target_city=None, target_state=None, target_zip=None,
                 target_country=None, target_notes=None):
        self.stinkbait_instance_id = stinkbait_session[1][3]
        self.boto_session = stinkbait_session[1][0]
        self.target_email = target_email
        self.target_name = target_name
        self.target_org = target_org
        self.target_title = target_title
        self.target_phone = target_phone
        self.target_address = target_address
        self.target_city = target_city
        self.target_state = target_state
        self.target_zip = target_zip
        self.target_country = target_country
        self.target_notes = target_notes

        # check if the target table exists
        target_table_name = f'stinkbait-targets-{self.stinkbait_instance_id}'
        available_regions = boto3.session.Session().get_available_regions('dynamodb')
        self.dynamodb = None
        for region in available_regions:
            try:
                self.dynamodb = self.boto_session.client('dynamodb', region_name=region)
                self.dynamodb.describe_table(TableName=target_table_name)
                break
            except:
                continue
        if not self.dynamodb:
            self.dynamodb = self.boto_session.client('dynamodb')
            self.dynamodb.create_table(
                TableName=target_table_name,
                KeySchema=[
                    {
                        'AttributeName': 'target_email',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'target_email',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )

    def add_target(self):
        table_name = "stinkbait-targets-" + self.stinkbait_instance_id
        dynamodb = self.stinkbait_session[1][0].client("dynamodb")

        try:
            response = dynamodb.put_item(
                TableName=table_name,
                Item={
                    "target_email": {"S": self.target_email},
                    "target_name": {"S": self.target_name},
                    "target_org": {"S": self.target_org} if self.target_org else {"NULL": True},
                    "target_title": {"S": self.target_title} if self.target_title else {"NULL": True},
                    "target_phone": {"S": self.target_phone} if self.target_phone else {"NULL": True},
                    "target_address": {"S": self.target_address} if self.target_address else {"NULL": True},
                    "target_city": {"S": self.target_city} if self.target_city else {"NULL": True},
                    "target_state": {"S": self.target_state} if self.target_state else {"NULL": True},
                    "target_zip": {"S": self.target_zip} if self.target_zip else {"NULL": True},
                    "target_country": {"S": self.target_country} if self.target_country else {"NULL": True},
                    "target_notes": {"S": self.target_notes} if self.target_notes else {"NULL": True},
                },
            )
            return response
        except Exception as e:
            return str(e)


    def remove_target(self, target_email):
        table_name = f"stinkbait-targets-{self.stinkbait_instance_id}"
        dynamodb = self.stinkbait_session[1][0].client('dynamodb')
        try:
            response = dynamodb.delete_item(
                TableName=table_name,
                Key={
                    'target_email': {
                        'S': target_email
                    }
                }
            )
            print(f"Successfully removed target with email: {target_email}")
        except Exception as error:
            print(f"Failed to remove target with email: {target_email} due to error: {error}")

    def update_target(self, target_email, target_name=None, target_org=None, target_title=None,
                      target_phone=None, target_address=None, target_city=None, target_state=None,
                      target_zip=None, target_country=None, target_notes=None):
        try:
            response = self.table.get_item(
                Key={
                    'target_email': target_email
                }
            )
        except Exception as e:
            print(e.response['Error']['Message'])
            return None
        else:
            item = response.get('Item')
            if item is None:
                print(f"Target with email '{target_email}' not found.")
                return None
            else:
                if target_name is not None and target_name != item['target_name']:
                    item['target_name'] = target_name
                if target_org is not None and target_org != item['target_org']:
                    item['target_org'] = target_org
                if target_title is not None and target_title != item['target_title']:
                    item['target_title'] = target_title
                if target_phone is not None and target_phone != item['target_phone']:
                    item['target_phone'] = target_phone
                if target_address is not None and target_address != item['target_address']:
                    item['target_address'] = target_address
                if target_city is not None and target_city != item['target_city']:
                    item['target_city'] = target_city
                if target_state is not None and target_state != item['target_state']:
                    item['target_state'] = target_state
                if target_zip is not None and target_zip != item['target_zip']:
                    item['target_zip'] = target_zip
                if target_country is not None and target_country != item['target_country']:
                    item['target_country'] = target_country
                if target_notes is not None and target_notes != item['target_notes']:
                    item['target_notes'] = target_notes

                try:
                    self.table.put_item(Item=item)
                except Exception as e:
                    print(e.response['Error']['Message'])
                    return None
                else:
                    return item
class Campaign:
    """
    Create a new campaign in Stinkbait. A campaign is a collection of targets, sites, and emails.
    A campaign site is a website that is used to host phishing malware payloads. Examples can be found in "bait/sites".
    A campaign email is a template for a phishing lure. Examples can be found in "bait/mail".
    A site is generated using Lambda, Flask, and Jinja2. Static resources are hosted on S3 and served by CloudFront. A cloudformation template will be used for this.
    With no/minimal alterations, a campaign email can be sent to multiple targets. The campaign email is sent using SES.
    """
    def __init__(self, stinkbait_session, campaign_name, org, start_date, end_date=None):
        self.stinkbait_session = stinkbait_session
        self.campaign_name = campaign_name
        self.org = org
        self.start_date = start_date
        self.end_date = end_date
        self.targets = []
        
    def add_target(self, target):
        self.targets.append(target)

    def remove_target(self, target):
        self.targets.remove(target)

    def add_campaign(self):
        try:
            table = self.stinkbait_session.resource("dynamodb").Table("stinkbait_campaigns")
            table.put_item(
                Item={
                    "campaign_name": self.campaign_name,
                    "org": self.org,
                    "start_date": self.start_date,
                    "end_date": self.end_date,
                    "targets": self.targets
                }
            )
            return True
        except Exception as e:
            return str(e)
    
    def remove_campaign(self):
        try:
            table = self.stinkbait_session.resource("dynamodb").Table("stinkbait_campaigns")
            table.delete_item(
                Key={"campaign_name": self.campaign_name}
            )
            return True
        except Exception as e:
            return str(e)

    def update_campaign(self, **kwargs):
        try:
            table = self.stinkbait_session.resource("dynamodb").Table("stinkbait_campaigns")
            response = table.get_item(
                Key={"campaign_name": self.campaign_name}
            )
            if "Item" in response:
                if "org" in kwargs:
                    self.org = kwargs["org"]
                if "start_date" in kwargs:
                    self.start_date = kwargs["start_date"]
                if "end_date" in kwargs:
                    self.end_date = kwargs["end_date"]
                if "targets" in kwargs:
                    self.targets = kwargs["targets"]
                table.put_item(
                    Item={
                        "campaign_name": self.campaign_name,
                        "org": self.org,
                        "start_date": self.start_date,
                        "end_date": self.end_date,
                        "targets": self.targets
                    }
                )
                return True
            else:
                return "Campaign not found"
        except Exception as e:
            return str(e)

    def get_campaign(self):
        try:
            table = self.stinkbait_session.resource("dynamodb").Table("stinkbait_campaigns")
            response = table.get_item(
                Key={"campaign_name": self.campaign
                })
            if "Item" in response:
                self.org = response["Item"]["org"]
                self.start_date = response["Item"]["start_date"]
                self.end_date = response["Item"]["end_date"]
                self.targets = response["Item"]["targets"]
                return True
        except Exception as e:
            return str(e)
        
class Orgs:
    def __init__(self, stinkbait_session, org_name, org_address=None, org_city=None, org_state=None, org_zip=None, org_country=None, org_notes=None):
        """
        Create a new organization in Stinkbait. An organization is a collection of targets and campaigns. 
        An organization can have multiple users, but only one user can be the owner of the organization. 
        The owner of the organization can add other users to the organization and can delete the organization.
        The owner of the organization can also delete any targets or campaigns in the organization. 
        The owner of the organization can also delete any users in the organization except for themselves. 
        The owner of the organization can also delete themselves from the organization, but only if there are other users in the organization. 
        If the owner of the organization deletes themselves from the organization, then the organization will be deleted.

        The following parameters are required to initialize the class:
        stinkbait_session - the stinkbait user session object
        org_name - the name of the organization
        org_owner - the owner of the organization and the user who is creating the organization

        and the following parameters are optional:
        org_address - the address of the organization
        org_city - the city of the organization
        org_state - the state of the organization
        org_zip - the zip code of the organization
        org_country - the country of the organization
        org_notes - any notes about the organization

        The following methods are available:
        add_org - add an organization to the stinkbait_orgs table
        remove_org - remove an organization from the stinkbait_orgs table
        update_org - update an organization in the stinkbait_orgs table
        get_org - get an organization from the stinkbait_orgs table
        list_orgs - list all organizations in the stinkbait_orgs table
        ChatGPT Response Below:
        
        """
    def __init__(self, stinkbait_session, org_name, org_owner, org_address=None, org_city=None, org_state=None, org_zip=None, org_country=None, org_notes=None):
        self.stinkbait_session = stinkbait_session
        self.org_name = org_name
        self.org_owner = org_owner
        self.org_address = org_address
        self.org_city = org_city
        self.org_state = org_state
        self.org_zip = org_zip
        self.org_country = org_country
        self.org_notes = org_notes

        # Check if stinkbait_orgs table exists and create it if not
        self.dynamodb = self.stinkbait_session[1][0].client('dynamodb')
        self.table_name = f'stinkbait_orgs_{self.stinkbait_session[1][3]}'
        try:
            self.dynamodb.describe_table(TableName=self.table_name)
        except:
            ec2 = self.stinkbait_session[1][0].client('ec2')
            regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
            table_created = False
            for region in regions:
                try:
                    dynamodb = self.stinkbait_session[1][0].client('dynamodb', region_name=region)
                    dynamodb.describe_table(TableName=self.table_name)
                    self.dynamodb = dynamodb
                    table_created = True
                    break
                except:
                    continue
            if not table_created:
                self.dynamodb.create_table(
                    TableName=self.table_name,
                    KeySchema=[
                        {
                            'AttributeName': 'org_name',
                            'KeyType': 'HASH'
                        }
                    ],
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'org_name',
                            'AttributeType': 'S'
                        }
                    ],
                    ProvisionedThroughput={
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                )

    def add_org(self):
        try:
            table = self.stinkbait_session.resource("dynamodb").Table("stinkbait_orgs")
            response = table.put_item(
                Item={
                    "org_name": self.org_name,
                    "org_owner": self.org_owner,
                    "org_address": self.org_address,
                    "org_city": self.org_city,
                    "org_state": self.org_state,
                    "org_zip": self.org_zip,
                    "org_country": self.org_country,
                    "org_notes": self.org_notes,
                }
            )
            return response
        except Exception as e:
            print(f"Error adding organization: {e}")
            return False

    def remove_org(self, org_name):
        try:
            self.stinkbait_session.dynamodb.delete_item(
                TableName='stinkbait_orgs',
                Key={
                    'org_name': {
                        'S': org_name
                    }
                }
            )
            return True
        except Exception as e:
            print(f'Error deleting organization {org_name}: {e}')
            return False

    def update_org(self, org_address=None, org_city=None, org_state=None, org_zip=None, org_country=None, org_notes=None):
        try:
            if self.stinkbait_session.user == self.org_owner:
                org = self.get_org(self.org_name)
                if org is not None:
                    update_expression = 'SET'
                    expression_attribute_values = {}
                    if org_address is not None:
                        update_expression += ' org_address = :org_address,'
                        expression_attribute_values[':org_address'] = org_address
                    if org_city is not None:
                        update_expression += ' org_city = :org_city,'
                        expression_attribute_values[':org_city'] = org_city
                    if org_state is not None:
                        update_expression += ' org_state = :org_state,'
                        expression_attribute_values[':org_state'] = org_state
                    if org_zip is not None:
                        update_expression += ' org_zip = :org_zip,'
                        expression_attribute_values[':org_zip'] = org_zip
                    if org_country is not None:
                        update_expression += ' org_country = :org_country,'
                        expression_attribute_values[':org_country'] = org_country
                    if org_notes is not None:
                        update_expression += ' org_notes = :org_notes,'
                        expression_attribute_values[':org_notes'] = org_notes
                    
                    update_expression = update_expression[:-1]
                    self.stinkbait_session.dynamodb.update_item(
                        TableName='stinkbait_orgs',
                        Key={'org_name': {'S': self.org_name}},
                        UpdateExpression=update_expression,
                        ExpressionAttributeValues=expression_attribute_values
                    )
                    return True
                else:
                    raise Exception("Organization not found")
            else:
                raise Exception("Only the owner of the organization can perform updates")
        except Exception as e:
            return str(e)

    def get_org(self, org_name):
        try:
            response = self.stinkbait_session.dynamodb.get_item(
                TableName=self.stinkbait_orgs_table,
                Key={'org_name': {'S': org_name}}
            )
        except Exception as e:
            print(f"Error getting org: {e}")
            return None
        
        if 'Item' in response:
            item = response['Item']
            org = {
                'org_name': item['org_name']['S'],
                'org_owner': item['org_owner']['S'],
                'org_address': item.get('org_address', {'S': ''})['S'],
                'org_city': item.get('org_city', {'S': ''})['S'],
                'org_state': item.get('org_state', {'S': ''})['S'],
                'org_zip': item.get('org_zip', {'S': ''})['S'],
                'org_country': item.get('org_country', {'S': ''})['S'],
                'org_notes': item.get('org_notes', {'S': ''})['S']
            }
            return org
        else:
            print(f"Org not found: {org_name}")
            return None


    def list_orgs(self):
        try:
            orgs = self.stinkbait_session.dynamodb.table('stinkbait_orgs').scan()['Items']
            return orgs
        except Exception as error:
            print(f"An error occurred while listing organizations: {error}")
            return None
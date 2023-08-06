import uuid
import configparser
import boto3

config = configparser.ConfigParser()
config.read("config.ini")

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("stinkbait_users")

class StinkBaitUser:
    def __init__(self, user_id=None, email=None, slack_username=None, discord_username=None, teams_username=None, phone_number=None):
        self.user_id = user_id or config.get("User", "user_id")
        if not self.user_id:
            self.user_id = self.create_user_id()
        self.email = email
        if not self.email:
            self.email = self.get_email()
        self.slack_username = slack_username
        self.discord_username = discord_username
        self.teams_username = teams_username
        self.phone_number = phone_number

        self.optional_attributes = [
            ("Slack username", self.slack_username),
            ("Discord username", self.discord_username),
            ("Teams username", self.teams_username),
            ("Phone number", self.phone_number),
        ]
        self.add_user_to_table()
    
    def create_user_id(self):
        user_id = str(uuid.uuid4())
        config.set("User", "user_id", user_id)
        with open("config.ini", "w") as configfile:
            config.write(configfile)
        return user_id
    
    def get_email(self):
        email = input("Please enter your email: ")
        return email
    
    def add_user_to_table(self):
        item = {
            "user_id": self.user_id,
            "email": self.email,
        }
        for attribute_name, attribute_value in self.optional_attributes:
            if attribute_value:
                item[attribute_name.lower().replace(" ", "_")] = attribute_value
        table.put_item(Item=item)
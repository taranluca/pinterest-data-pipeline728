import yaml
import requests
from time import sleep
import random
from multiprocessing import Process
import boto3
import json
import sqlalchemy
from sqlalchemy import text


random.seed(100)
                
invoke_url_pin = "https://humxtjcumb.execute-api.us-east-1.amazonaws.com/test/streams/streaming-0afffbed4f09-pin/record"
invoke_url_geo = "https://humxtjcumb.execute-api.us-east-1.amazonaws.com/test/streams/streaming-0afffbed4f09-geo/record"
invoke_url_user = "https://humxtjcumb.execute-api.us-east-1.amazonaws.com/test/streams/streaming-0afffbed4f09-user/record"

class AWSDBConnector:

    def __init__(self,filename):
        self.filename = filename

    def read_db_creds(self):
        with open(self.filename,"r") as file:
            cred_file = yaml.safe_load(file)
        return cred_file
        
    def create_db_connector(self):
        creds = self.read_db_creds()
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{creds["USER"]}:{creds["PASSWORD"]}@{creds["HOST"]}:{creds["PORT"]}/{creds["DATABASE"]}?charset=utf8mb4")
        return engine


new_connector = AWSDBConnector("db_creds.yaml")


def run_infinite_post_data_loop():
    while True:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()

        with engine.connect() as connection:

            pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
            pin_selected_row = connection.execute(pin_string)
            
            for row in pin_selected_row:
                pin_result = dict(row._mapping)

            geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            
            for row in geo_selected_row:
                geo_result = dict(row._mapping)

            user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            
            for row in user_selected_row:
                user_result = dict(row._mapping)
            

            payload_pin = json.dumps({
                    "StreamName": "streaming-0afffbed4f09-pin",
                    "Data": {     
                            "index": pin_result["index"],'unique_id': pin_result['unique_id'], 'title': pin_result['title'], 'description': pin_result['description'], 
                            'poster_name': pin_result['poster_name'], 'follower_count': pin_result['follower_count'], 'tag_list': pin_result['tag_list'], 'is_image_or_video': pin_result['is_image_or_video'],
                            'image_src': pin_result['image_src'], 'downloaded': pin_result['downloaded'], 'save_location': pin_result['save_location'], 'category': pin_result['category']
                            },
                            "PartitionKey": "Partition-pin"
                }
                
                )

            headers = {'Content-Type': 'application/json'}
            response_pin = requests.request("PUT", invoke_url_pin, headers=headers, data=payload_pin)
            print(f"pin {response_pin.status_code}")


            payload_geo = json.dumps({
                    "StreamName": "streaming-0afffbed4f09-geo",
                    "Data": {     
                            'ind': geo_result['ind'], 'timestamp': geo_result['timestamp'], 'latitude': geo_result['latitude'], 'longitude': geo_result['longitude'], 'country': geo_result['country']
                            },
                            "PartitionKey": "Partition-geo"
                }
                    
                ,default=str)

            headers = {'Content-Type': 'application/json'}
            response_geo = requests.request("PUT", invoke_url_geo, headers=headers, data=payload_geo)
            print(f"geo {response_geo.status_code}")            


            payload_user = json.dumps({
                    "StreamName": "streaming-0afffbed4f09-user",
                    "Data": {     
                            'ind': user_result['ind'], 'first_name': user_result['first_name'], 'last_name': user_result['last_name'], 'age': user_result['age'], 'date_joined': user_result['date_joined']
                            },
                            "PartitionKey": "Partition-user"
                }
                    
                ,default=str)


            headers = {'Content-Type': 'application/json'}
            response_user = requests.request("PUT", invoke_url_user, headers=headers, data=payload_user)
            print(f"user {response_user.status_code}")




if __name__ == "__main__":
    run_infinite_post_data_loop()
    print('Working')
    

from datetime import datetime

from database import db
from models import EventRegistration, EventUpdate, Register, Deregister
from aws_models import AWSConnection
from config import config_data


#######################################################
############# Initializa the S3 resource ##############
#######################################################

s3_bucket = AWSConnection(bucket=config_data['BUCKET_NAME_TO'],
                          access_key=config_data['AWS_ACCESS_KEY'],
                          access_secret=config_data['AWS_ACCESS_SECRET'],
                          resource='s3')

#######################################################
##### Get all the folders in the S3 Loka Data lake ####
#######################################################

folders = s3_bucket.list_folders_s3_bucket()

#######################################################
### Get all the files name in the S3 Loka Data lake ###
#######################################################

filesname = dict()
for folder in folders:
    files = s3_bucket.list_sorted_object_s3_bucket(prefix= folder)
    filesname['folder'] = folder
    filesname['filesnames'] = files


#######################################################
##### Get all the files in the S3 Loka Data lake ######
#######################################################
stg_events = list()

for filename in filesname['filesnames']:
    file_content_json = s3_bucket.get_file_s3_bucket(
        filename=f'{filesname["folder"]}/{filename}')
    for event in file_content_json:
        stg_row = dict()
        if event['event'] == 'register':
            stg_row['event'] = event['event']
            stg_row['on'] = event['on']
            stg_row['id'] = event['data']['id']
            stg_row['register_at'] = event['at']
            stg_events.append(stg_row)
        
        if event['event'] == 'deregister':
            stg_row['event'] = event['event']
            stg_row['on'] = event['on']
            stg_row['id'] = event['data']['id']
            stg_row['deregister_at'] = event['at']
            stg_events.append(stg_row)

        if event['event'] == 'update':
            stg_row['event'] = event['event']
            stg_row['on'] = event['on']
            stg_row['id'] = event['data']['id']
            stg_row['lat'] = event['data']['location']['lat']
            stg_row['lng'] = event['data']['location']['lng']
            stg_row['at'] = event['data']['location']['at']
            stg_row['organization_id'] = event['organization_id']
            stg_events.append(stg_row)

register_list = []
deregister_list = []
event_registration = []
event_updates = []
locations = []

for element in stg_events:
    if element['event'] == 'register':
        instance_register = Register(element['id'], element['register_at'])
        register_list.append(instance_register)

    if element['event'] == 'deregister':
        instance_deregister = Deregister(element['id'], element['deregister_at'])
        deregister_list.append(instance_deregister)

    if element['event'] == 'update':
        instance_registration = EventRegistration(
            event = element['event'],
            on = element['on'],
            id = element['id'],
            register_at= None,
            deregister_at= None,
            organization_id= element['organization_id'])
        
        event_registration.append(instance_registration)

        instance_update = EventUpdate(
            element['id'],
            element['lat'],
            element['lng'],
            element['at']
        )

        event_updates.append(instance_update)

for eventRegistration in event_registration:
    for register in register_list:
        if eventRegistration.id == register.id:
            eventRegistration.register_at = register.register_at
    for deregister in deregister_list:
        if eventRegistration.id == deregister.id:
            eventRegistration.deregister_at = deregister.deregister_at

#### REMOVING DUPLICATES ON event_registration list (I need to review why I produce duplicates on the previous Loop) ####
registration_seen_id = set()
unique_events_registration = []
for obj in event_registration:
    if obj.id not in registration_seen_id:
        unique_events_registration.append(obj)
        registration_seen_id.add(obj.id)

##### Bulk update of all the registration objects #####
db.bulk_save_objects(unique_events_registration)
db.commit()
db.flush()
db.close()

##### Bulk update of all the updates objects #####
db.bulk_save_objects(event_updates)
db.commit()
db.flush()
db.close()

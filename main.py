import functions_framework
from util import pharmacy_map as PM
from urllib.parse import quote
from twilio.rest import Client
from flask import jsonify
import yaml
import os

def load_yaml_file(filepath):
    with open(filepath, 'r') as file:
        data = yaml.safe_load(file)
    return data

# Use the function to load the configuration
config = load_yaml_file('config.yaml')

env = os.getenv("deployment_env")

# initialize twilio client for SMS
TWILIO_ACCOUNT_SID = config[env]["twilio"]["account_sid"] 
TWILIO_AUTH_TOKEN = config[env]["twilio"]["auth_token"] 
TWILIO_PHONE_NUMBER = config[env]["twilio"]["phone_number"] 

CF_TRANSFER_CALL = config[env]["cloud_functions"]["transfer_call"]

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

"""
{
    'call_uuid': 'cdfbeb4b-00c2-44eb-ae91-00e83584f6f7', 
    'request_uuid': 'edc91c3d-0387-42c8-9315-8c2ab1e33127', 
    'name': 'Focalin', 
    'dosage': '10', 
    'brand': 'Generic', 
    'quantity': '30', 
    'type': 'Extended Release', 
    'pharm_phone': '+12032248444'}
"""
@functions_framework.http
def main(request):
    
    #pass in pharm name as we will use this for extensions later
    try:
        request_json = request.get_json()
        
        call_uuid = request_json["call_uuid"]
        request_uuid = request_json["request_uuid"]
        name = request_json["name"]
        dosage = request_json["dosage"]
        brand = request_json["brand"]
        quantity = request_json["quantity"]
        release_type = request_json["type"]
        pharm_phone = request_json["pharm_phone"]
        
        parameters = {
            "call_uuid": call_uuid, # pass the uuid, this will become metadata on the actual request 
            "request_uuid": request_uuid,
            "name": name,
            "dosage": dosage,
            "brand": brand,
            "quantity": quantity,
            "type": release_type
        }
        
        # Convert parameters to URL query string 
        query_string = "&amp;".join([f"{key}={quote(value)}" for key, value in parameters.items()])


        # TwiML
        twiml = f"""
        <Response>
            <Play digits="{PM.EXT_CVS}"></Play>
            <Redirect>{CF_TRANSFER_CALL}?{query_string}</Redirect>
        </Response>
        """

        twilio_client.calls.create(
            twiml=twiml,  # TwiML content as URL data
            to=pharm_phone,
            from_= TWILIO_PHONE_NUMBER
        )
        # call plased succesfully
        return jsonify({'message': 'Successfully started call.'}), 200
    except Exception as e:
        print({"error": "Failed while placing the call ", "exception": str(e)})
        return jsonify({'error': 'Calling pharmacies Failed', 'exception': str(e)}), 500
   






        
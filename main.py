import functions_framework
from flask import jsonify, request
from firebase_admin import credentials, firestore, auth, initialize_app
import twilio
from twilio.rest import Client
import json


# Initialize Firebase Admin SDK with the service account key
cred = credentials.Certificate("firebase_creds.json")  # Update with your service account key file 
initialize_app(cred)
db = firestore.client() # set firestore client

# initialize twilio client for SMS
ACCOUNT_SID = 'AC3d433258fe9b280b01ba83afe272f438'
AUTH_TOKEN = '2cc106ae7b360c99a7be11cc4ea77c07'
twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)

"""
{
    "user_session_token": "12345abcde",
    "phone_number": "+12032248444",
    "user_location": "Troy, NY",
    "prescription": {
        "name": "Focalin",
        "dosage": "10",
        "brand_or_generic": "Generic",
        "quantity": "30",
        "type": "Extended%20Release"
    }
}
"""
@functions_framework.http
def main(request):
    request_json = request.get_json()
    
    print(request_json)
    
    # request_json["call_uuid"]

    
    # #pass in pharm name as we will use this for extensions later
    # try:
    #     parameters = {
    #         "call_uuid": call_uuid, # pass the uuid, this will become metadata on the actual request
    #         "request_uuid": search_uuid,
    #         "name": prescription["name"],
    #         "dosage": prescription["dosage"],
    #         "brand": prescription["brand_or_generic"],
    #         "quantity": prescription["quantity"],
    #         "type": prescription["type"]
    #     }
        
    #     # Convert parameters to URL query string 
    #     query_string = "&amp;".join([f"{key}={quote(value)}" for key, value in parameters.items()])


    #     # TwiML
    #     twiml = f"""
    #     <Response>
    #         <Play digits="{PM.EXT_CVS}"></Play>
    #         <Redirect>https://us-central1-rxradar.cloudfunctions.net/transfer-twilio-bland?{query_string}</Redirect>
    #     </Response>
    #     """

    #     """
    #     Note: in cloud function, extract url params like:
    #         name = request.args.get('name')
    #         dosage = request.args.get('dosage')
    #         brand = request.args.get('brand')
    #         quantity = request.args.get('quantity')
    #         medication_type = request.args.get('type')
    #     """

    #     client.calls.create(
    #         twiml=twiml,  # TwiML content as URL data
    #         to=pharm_phone,
    #         from_='+18337034125'
    #     )
    #     # call plased succesfully
    #     return True
    # except Exception as e:
    #     print({"error": "Failed while placing hte call ", "exception": str(e)})
    #     return  False
   






        
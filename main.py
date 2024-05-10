import functions_framework
from util import pharmacy_map as PM
from urllib.parse import quote
from twilio.rest import Client
from flask import jsonify

# initialize twilio client for SMS
ACCOUNT_SID = 'AC3d433258fe9b280b01ba83afe272f438'
AUTH_TOKEN = '2cc106ae7b360c99a7be11cc4ea77c07'
twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)

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
            <Play digits="{PM.EXT_TEST}"></Play>
            <Redirect>https://us-central1-rxradar.cloudfunctions.net/dev-transfer-twilio-bland?{query_string}</Redirect>
        </Response>
        """

        """
        Note: in cloud function, extract url params like:
            name = request.args.get('name')
            dosage = request.args.get('dosage')
            brand = request.args.get('brand')
            quantity = request.args.get('quantity')
            medication_type = request.args.get('type')
        """

        twilio_client.calls.create(
            twiml=twiml,  # TwiML content as URL data
            to=pharm_phone,
            from_='+18337034125'
        )
        # call plased succesfully
        return jsonify({'message': 'Successfully started call.'}), 200
    except Exception as e:
        print({"error": "Failed while placing hte call ", "exception": str(e)})
        return jsonify({'error': 'Calling pharmacies Failed', 'exception': str(e)}), 500
   






        
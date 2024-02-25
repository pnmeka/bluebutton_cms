#pip install cms-bluebutton-sdk
#this will launch flask, allow you to download data from cms after oauth login. create a report.html and show the file

#launches oauth for bbtn
from cms_bluebutton import BlueButton, AuthorizationToken
from flask import Flask, redirect, render_template, request, session, url_for, jsonify
import os, subprocess
import requests, json

# initialize the app
app = Flask(__name__)

# Instantiate SDK class instance via conf in file
bb = BlueButton("my_bb2_sdk_conf.json")

# auth_data is saved for the current user
auth_data = bb.generate_auth_data()

"""
AuthorizationToken holds access grant info:
  access token, expire in, expire at, token type, scope, refreh token, etc.
It is associated with current logged in user in real app.
Check SDK python docs for more details.
"""

auth_token = None

# Start authorize flow: Response with URL to redirect to Medicare.gov beneficiary login
@app.route("/", methods=["GET"])
def get_auth_url():
    auth_url = bb.generate_authorize_url(auth_data)
    return redirect(auth_url)

        
@app.route('/api/bluebutton/callback/', methods=['GET'])
def authorization_callback():
    request_query = request.args
    code = request_query.get('code')   
    state = request_query.get('state')
    

    auth_token = bb.get_authorization_token(auth_data, code, state)

    """
    Now access token obtained.

    Note: During authorization, the beneficiary can grant
    access to their demographic data and claims data or only claims data.

    Check the scope
    of the current access token as shown below:
    """
    scopes = auth_token.scope

    # iterate scope entries here or check if a permission is in the scope
    if "patient/Patient.read" in scopes: 
        # patient info access granted
        print("Access to patient info granted.")
    else:
        print("Access to patient info not granted.")
    
    required_scopes = {"patient/Coverage.read", "patient/ExplanationOfBenefit.read", "patient/Patient.read", "profile"}
    granted_scopes = set(scopes)  # Convert list of scopes to a set for this operation

    if required_scopes.issubset(granted_scopes):
        # All required scopes are granted
        print("Access to all required scopes granted.")
    else:
        # Not all required scopes are granted
        missing_scopes = required_scopes - granted_scopes
        print(f"Missing access to required scopes: {missing_scopes}")
       
    config = {
        "auth_token": auth_token,
        "params": {},
        "url": "https://sandbox.bluebutton.cms.gov/v2/connect/userinfo"
    }

    result = {}

    # fetch eob, patient, coverage, profile
    try:
        eob_data = bb.get_explaination_of_benefit_data(config)
        result['eob_data'] = eob_data['response'].json()
        eob_data = eob_data['response'].json()
        result['eob_data'] = eob_data

        # A FHIR search response can result in a large number of resources. 
        # For example, an EOB search of a beneficiary could return hundreds 
        # of resources. By default, search results are grouped into
        # pages with 10 resources each. For example, 
        # bb.get_explaination_of_benefit_data(config) returns the
        # first page of resources as a FHIR bundle with a link section 
        # of page navigation URLs. Pagination link names include 
        # 'first,' 'last,' 'self,' next,' and 'previous.' 
        # To get all the pages, use bb.get_pages(data, config)
     
        
        eob_pages = bb.get_pages(eob_data, config)
        result['eob_pages'] = eob_pages['pages']
        auth_token = eob_pages['auth_token']

        pt_data = bb.get_patient_data(config)
        result['patient_data'] = pt_data['response'].json()

        coverage_data = bb.get_coverage_data(config)
        result['coverage_data'] = coverage_data['response'].json()

        profile_data = bb.get_profile_data(config)
        result['profile_data'] = profile_data['response'].json()
        
        with open('response_cms.json', 'w') as file:
            json.dump(result, file, indent=4)
        subprocess.run(["python", "extract_data.py"])
    except Exception as ex:
        print(ex)

    return redirect(url_for('static', filename='report.html'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3015)

# bluebutton_cms

This repo allows you to access claims data of a medicare subscriber and to filter data to allow understanding it.

Flask server -> Oauth login -> collect claims via API -> save data -> filter data -> show as html

About Bluebutton:
Integration with Blue Button 2.0 provides value to organizations that deliver services to people with Medicare.
People with Medicare can allow access to their data, which can improve data accuracy and efficiency over manual data entry. Faster, more accurate data can lead to better service recommendations and health outcomes for beneficiaries. 

Learn more at:

    https://bluebutton.cms.gov/

Step 1 - Get Sandbox credentials: 

1. First go here to set up an free account:

        https://sandbox.bluebutton.cms.gov/v1/accounts/create

2. After you create an account login. Click on 'Add an Application'
3. Enter following credentials to get set up:

       OAuth - Client Type: confidential
       OAuth - Grant Type: authorization-code
       Callback URLS / Redirect Uris: http://localhost:3015/api/bluebutton/callback/
4. Save and you should receive a Client ID and Client Secret.

Step 2- Git clone and launch Flask server

5. Git clone this repo

       git clone https://github.com/pnmeka/bluebutton_cms/
6. Set up required modules

       pip install -r requirements.txt


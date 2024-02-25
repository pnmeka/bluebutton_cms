**# bluebutton_cms sandbox
**
This repo allows you to access claims data of a medicare subscriber and to filter data to allow understanding it.

Flask server -> Oauth login -> collect claims via API -> save data -> filter data -> show as html

About Bluebutton:
Integration with Blue Button 2.0 provides value to organizations that deliver services to people with Medicare.
People with Medicare can allow access to their data, which can improve data accuracy and efficiency over manual data entry. Faster, more accurate data can lead to better service recommendations and health outcomes for beneficiaries. 

Learn more at:

    https://bluebutton.cms.gov/

**Step 1 - Get Sandbox credentials:** 

1. First go here to set up an free account:

        https://sandbox.bluebutton.cms.gov/v1/accounts/create

2. After you create an account login. Click on 'Add an Application'
3. Enter following credentials to get set up:

       OAuth - Client Type: confidential
       OAuth - Grant Type: authorization-code
       Callback URLS / Redirect Uris: http://localhost:3015/api/bluebutton/callback/
4. Save and you should receive a Client ID and Client Secret.

**Step 2- Git clone and launch Flask server**

5. Git clone this repo

       git clone https://github.com/pnmeka/bluebutton_cms/
       cd bluebutton_cms

7. Update the credentials in config file.

        open my_bb2_sdk_conf.json and enter your saved Client ID and secret and save
       
8. Set up required modules for your server

       pip install -r requirements.txt

9. Launch Flask server

       python3 bbtn.py

10. launch a webbrowser and go to port 3015 by entering the following in addressbar

           localhost:3015
    
12. It should automatically take you to oauth login to allow download of claims. Enter the follwoing dummy credentials

        user:BBUser00000
        pwd:PW00000!
    Click Login. Once logged in, accept to receive all claims data.

13. This should automatically lead to downloading the claims data as response_cms.json. Then extract_data.py will filter data
    and make a file static/report.html and show that file in browser.
15. YOU ARE ALL SET!

**DEBUGGING**
a. Clear browser history if you are able to login but the data isnt downloading. Instead you get a 404 error

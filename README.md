# Reddit SMS Alerts

A server-side script to scrape Reddit communities in real time and send SMS alerts when posts of interests are detected
    pip install -r requirements.txt

# Usage

    from detect import Detector
    spy = Detector('FREE', 'gift card')
    spy.loop()
The code above creates a web-scraper that will watch the r/FREE subreddit and sends SMS messages when posts with 'gift card' in the title are detected.
# Config
Inside the [config.py](https://github.com/BrianSantoso/reddit-sms/blob/master/config.py) file, you will find the following parameters which you should configure to your Reddit (https://www.reddit.com/prefs/apps) and Twilio (https://www.twilio.com/console) developer accounts:
    
    REDDIT_CLIENT_ID = 'Your reddit client id'
    REDDIT_CLIENT_SECRET = 'Your reddit client secret'
    REDDIT_USERNAME = 'Reddit username'
    REDDIT_PASSWORD = 'Reddit password'
    
    TWILIO_ACCOUNT_SID = 'Twilio account SID'
    TWILIO_AUTH_TOKEN = 'Twilio authentication token'
    TWILIO_PHONE = 'Your Twilio Number'
    RECEIVING_PHONE = 'The phone number which will receive the SMS text messages'
    
# Dependencies
To install all python dependencies:

    pip install -r requirements.txt
    
You will also need to configure the following (See above about Config)
* Reddit API
* Twilio API

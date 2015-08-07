# django-admin-twitter
Manage twitter from Django admin interface

##Disclaimer

I hold no liability for what you do with this administration interface or what happens to you by using it. Abusing the Twitter API *can* get you banned from Twitter, so make sure to read up on [proper usage](https://support.twitter.com/articles/76915-automation-rules-and-best-practices) of the Twitter API.

**Do not mass reply, favorite or follow using this interface to avoid being banned**

##Dependencies

You will need to install Python's [python-twitter](https://github.com/sixohsix/twitter/) library:

    pip install twitter

Although this library should be installed along with the Twitter Follow Bot if you used `pip`.

You will also need to create an app account on https://dev.twitter.com/apps

1. Sign in with your Twitter account
2. Create a new app account
3. Modify the settings for that app account to allow read & write
4. Generate a new OAuth token with those permissions

Following these steps will create 4 tokens that you will need to place in _settings.py_ as discussed bellow.

##Installation

- Copy the admin_twitter to your project's directory
- Add _admin___twitter to INSTALLED_APPS on your _settings.py_
- Add OAUTH_TOKEN , OAUTH_SECRET , CONSUMER_KEY and CONSUMER_SECRET to your _settings.py_ (follow the instructions on the Dependencies section)
- Copy _updatebutton.js_ to your static directory
- Update your db (manage.py makemigrations;manage.py migrate)

##Usage
- On your admin interface under the Admin_Twitter section you will find the 3 components of admin_twitter:
 - **Authors** - Users from who you have fetched tweets
 - **Messages** - Messages that can be sent to users
 - **Tweets** - List of fetched tweets
 
- To start using Admin_Twitter go to **Tweets** and press **Update Tweets** (If you can't see the button on the top right corner, check that _updatebutton.js_ is being correctly loaded). You'll be asked for the search pattern for the tweets and the corresponding tweets will be added to Tweet list and the corresponding users will be added to the Author list.
- From the Tweet list you can favourite tweets or reply to tweets - a random Message will be used for each reply (make sure to have at least one active message on the Message list) by selecting the Tweets and using the dropdown menu.
- From the Author list you can follow users by selecting them and using the dropdown menu.
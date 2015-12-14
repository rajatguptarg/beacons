Beacon Management Portal
=========================


[![Build Status](https://travis-ci.org/rajatguptarg/beacons.svg)](https://travis-ci.org/rajatguptarg/beacons)
[![Coverage Status](https://coveralls.io/repos/rajatguptarg/beacons/badge.svg?branch=master&service=github)](https://coveralls.io/github/rajatguptarg/beacons?branch=master)
[![Code Climate](https://codeclimate.com/github/rajatguptarg/beacons/badges/gpa.svg)](https://codeclimate.com/github/rajatguptarg/beacons)
[![PyPI version](https://badge.fury.io/py/my_beacon_manager.svg)](https://badge.fury.io/py/my_beacon_manager)
[![Code Health](https://landscape.io/github/rajatguptarg/beacons/master/landscape.svg?style=flat)](https://landscape.io/github/rajatguptarg/beacons/master)


This is basic web application to manage your beacons.


How to Run
==========
To run this app, we prefer to use **virtualenv**. Follow these steps to run
this application:

**[1]** Create the virtual environment

**[2]** Inside virtual env, fire this command `pip install -r requirements.txt`

**[3]** Now you are done, run your app by firing command `python run.py`

You also need to have to have your `client_secrets.json` file, which you will get by downloading the OAuth key of your project. Make sure to rename the name of the file as `client_secrets.json`. This file should look like `sample_client_secret.json` provided with the code.

Now your server is started, Go to browser and open the URL: `127.0.0.1:5000`

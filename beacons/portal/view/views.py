from flask import Blueprint, render_template, request
import flask
import requests
from oauth2client import client
import json
from config import LIST_BEACONS, SCOPE
from beacons.portal.controller import controller
from beacons.portal.helper import BeaconHelper

portal = Blueprint('portal', __name__)
session = requests.Session()
beacon_helper = BeaconHelper()


@portal.route('/')
def list_beacons():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials']
    )
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        auth_request = session.get(LIST_BEACONS,
            headers=beacon_helper.get_header(credentials.access_token))

        return render_template(
            'beacons.jinja', beacons=json.loads(auth_request.content)
        )


@portal.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope=SCOPE,
        redirect_uri=flask.url_for('portal.oauth2callback', _external=True),
    )

    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        return flask.redirect(flask.url_for('portal.list_beacons'))


@portal.route('/register', methods=['GET'])
def register_beacons():
    return render_template('register.jinja')


@portal.route('/register', methods=['POST'])
def register_beacons_status():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials']
    )
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        beacon = beacon_helper.create_beacon(request.form)
        data = controller.send_registration_request(beacon, credentials)
        return render_template('registration_status.jinja',
            status=json.loads(data)
        )


@portal.route('/unregister', methods=['GET'])
def unregister_beacons():
    return render_template('unregister.jinja')


@portal.route('/unregister', methods=['POST'])
def unregister_beacons_status():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials']
    )
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        beacon_details = beacon_helper.create_beacon_name(request.form)
        status = controller.send_deactivation_request(beacon_details,
            credentials)
        # TODO: Make proper status based upon respnse
        return render_template(
            'unregistration_status.jinja', status=status
        )

from flask import Blueprint, render_template, request
import flask
import requests
from oauth2client import client
import json
from config import SUCCESS, ERROR, LIST_BEACONS, SCOPE, REGISTER_BEACONS
from beacons import Beacon
from header import Header
from beacon_name import BeaconName

portal = Blueprint('portal', __name__)
session = requests.Session()


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
        header = Header(credentials.access_token)
        auth_request = session.get(
            LIST_BEACONS, headers=header.__str__()
        )

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


@portal.route('/register', methods=['GET', 'POST'])
def register_beacons():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials']
    )

    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        form = Beacon(request.form)
        if request.method == 'POST' and form.validate():
            request_body = Beacon.registration_request_body(form)
            header = Header(credentials.access_token)
            response = requests.post(
                REGISTER_BEACONS, data=json.dumps(request_body),
                headers=header.__str__()
            )
            return render_template('registration_status.jinja',
                status=json.loads(response.content)
            )

        return render_template('register.jinja', form=form)


@portal.route('/unregister', methods=['GET', 'POST'])
def unregister_beacons():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials']
    )
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        form = BeaconName(request.form)
        if request.method == 'POST' and form.validate():
            header = Header(credentials.access_token)
            url = BeaconName.get_deactivation_url(form)
            response = requests.post(url, headers=header.__str__())
            status = ERROR if response.status_code is 400 else SUCCESS

            return render_template(
                'unregistration_status.jinja', status=status
            )

        return render_template('unregister.jinja', form=form)

from flask import Blueprint, render_template, request
from flask.ext.session import Session
import flask
import requests
from oauth2client import client
import json

portal = Blueprint('portal', __name__)
sess = Session()
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
        auth_request = session.get(
            'https://proximitybeacon.googleapis.com/v1beta1/beacons',
            headers={
                'Authorization': 'Bearer ' + credentials.access_token
            }
        )
        return render_template(
            'beacons.jinja', beacons=json.loads(auth_request.content)
        )


@portal.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope='https://www.googleapis.com/auth/userlocation.beacon.registry',
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


@portal.route('/register')
def register_beacons():
    return render_template('register.jinja')


@portal.route('/unregister')
def unregister_beacons():
    return render_template('unregister.jinja')


@portal.route('/registration-status', methods=['POST'])
def beacon_registration_status():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials']
    )

    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        advertised_id = request.form.get('advid')
        status = request.form.get('status')
        beacon_type = request.form.get('type')

        request_body = {
            "advertisedId": {
                "type": beacon_type,
                "id": advertised_id,
            },
            "status": status,
        }

        header = {
            'Authorization': 'Bearer ' + credentials.access_token
        }

        response = requests.post(
            'https://proximitybeacon.googleapis.com/v1beta1/beacons:register',
            data=json.dumps(request_body),
            headers=header
        )

        if response.status_code == 400:
            return render_template(
                'registration_status.jinja',
                status=json.loads(response.content)['error']
            )

        return render_template(
            'registration_status.jinja',
            status=json.loads(response.content)['success']
        )


@portal.route('/unregistration-status', methods=['POST'])
def beacon_unregistration_status():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials']
    )

    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        beacon_name = request.form.get('name')

        header = {
            'Authorization': 'Bearer ' + credentials.access_token
        }

        url = 'https://proximitybeacon.googleapis.com/v1beta1/'
        url += beacon_name + ':deactivate'

        response = requests.post(url, headers=header)

        if response.status_code == 400:
            return render_template(
                'unregistration_status.jinja',
                status='ERROR'
            )

        return render_template(
            'unregistration_status.jinja',
            status='SUCCESS'
        )

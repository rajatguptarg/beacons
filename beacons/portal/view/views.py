from flask import Blueprint, flash, render_template, request
from flask.ext.session import Session
import flask
import requests
from oauth2client import client
import json
from config import LIST_BEACONS, SCOPE, ATTACHMENT
from beacons.portal.controller import controller
from beacons.portal.models import Beacon, Header
from beacons.portal.models import Beacon, BeaconName, Header

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
        auth_request = session.get(LIST_BEACONS,
            headers=header.get_header_body())

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

@portal.route('/attachment')
def attachment_beacons():
    return render_template('attachment.jinja')

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
        beacon = Beacon(request.form)
        data = controller.register_beacon(beacon, credentials)
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
        beacon = Beacon(request.form)
        status = controller.deactivate_beacon(beacon, credentials)
        # TODO: Make proper status based upon respnse
        return render_template(
            'unregistration_status.jinja', status=status
        )


@portal.route('/edit', methods=['POST'])
def edit_beacon():
    return render_template(
        'edit_beacon.jinja', beacon=request.form.get('name'),
        advid=request.form.get('advid')
    )


@portal.route('/edit-status', methods=['POST'])
def edit_beacon_status():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials']
    )
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        beacon_details = Beacon(request.form)
        status = controller.modify_beacon(beacon_details, credentials)

        # TODO: Make proper status based upon respnse
        return render_template(
            'edit_beacon_status.jinja', status=status
        )

@portal.route('/namespace', methods=['GET'])
def beacon_namespace():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials']
    )

    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        header = Header(credentials.access_token)
        response = requests.get(ATTACHMENT,
            headers=header.__str__())

        return render_template(
            'namespace_status.jinja', status=json.loads(response.content)
        )


@portal.route('/attachment-status', methods=['POST'])
def beacon_attachment_status():
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        beacon = Beacon(request.form.get('advid'))
        beacon.name = request.form.get('name')
        beacon.msg = request.form.get('msg')

        try:
            json_object = json.loads(beacon.msg)
        except ValueError, e:
            flash('Invalid Input')

        request_body = beacon.attachment_request_body()
        header = Header(credentials.access_token)
        url = config.ATTACH_BEACONS + beacon.name + config.ATTACH
        response = requests.post(
            url, data=(json.dumps(request_body)),
            headers=header.__str__()
            )
        status1 = json.loads(response.content)
        for key, value in status1.iteritems():
            if(key == 'data'):
                ans = base64.b64decode(status1[key])
                finalans = json.loads(ans)
        return render_template(
            'attachment_status.jinja', status1=finalans,
            status=json.loads(response.content)
        )


from flask import Blueprint, render_template, flash, request
import flask
import requests
from oauth2client import client
import json
import base64
from config import SCOPE, ATTACHMENT, SUCCESS, ERROR
from beacons.portal.controller import controller
from beacons.portal.models import Beacon, Header
import beacons


portal = Blueprint('portal', __name__)
session = requests.Session()


@portal.errorhandler(ValueError)
def page_not_found(e):
    beacons.app.logger.error(e)


@portal.route('/')
def list_beacons():
    if 'credentials' not in flask.session:
        beacons.app.logger.info('Creating the new session.')
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials']
    )

    if credentials.access_token_expired:
        beacons.app.logger.info('Session Expired. Login Agained.')
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        beacon = controller.list_beacons(credentials)
        return render_template('beacons.jinja', beacons=beacon)


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
        beacon = Beacon(request.form)
        data = controller.register_beacon(beacon, credentials)
        name = controller.get_session_username(credentials)
        if data.get('error'):
            beacons.app.logger.warning('USER: ' + name + '\nBeacon with ' +
                str(beacon) + ' failed to register.')
        else:
            beacons.app.logger.info('USER: ' + name +
                '\nBeacon with ' + str(beacon) + ' registered successfully.')
        return render_template(
            'registration_status.jinja', status=data)


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
        user = controller.get_session_username(credentials)
        # TODO: Make proper status based upon respnse
        beacons.app.logger.info('USER: ' + user + '\nBeacon with ' +
            str(beacon) + ' unregistration successful.')
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
        beacon = Beacon(request.form)
        user = controller.get_session_username(credentials)
        status = controller.modify_beacon(beacon, credentials)
        status = SUCCESS if status.get('beaconName') else ERROR
        if status == SUCCESS:
            beacons.app.logger.info('USER:' + user + '\nModified beacon' +
            ' with ' + str(beacon) + 'successfully.')
        else:
            beacons.app.logger.warning('USER:' + user + '\nModified beacon' +
                ' with ' + str(beacon) + ' failed.')
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


@portal.route('/attachment')
def attachment_beacons():
    return render_template('attachment.jinja')


@portal.route('/attachment-status', methods=['POST'])
def beacon_attachment_status():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials']
    )

    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        beacon = Beacon(request.form)
        status = controller.attach_data_to_beacon(beacon, credentials)
        user = controller.get_session_username(credentials)
        try:
            json.loads(request.form['msg'])
            beacons.app.logger.info('USER:' + user + '\nAdded attachement to' +
                ' beacon with ' + str(beacon) + ' successfully.')
        except ValueError:
            beacons.app.logger.error('USER:' + user + '\nAdded attachement' +
                ' to beacon with ' + str(beacon) + ' raised valued error.')
            flash('Invalid Input !!!!')
            return flask.redirect(flask.url_for('portal.attachment_beacons'))

        ans = base64.b64decode((json.loads(status))['data'])
        finalans = json.loads(ans)
        return render_template(
            'attachment_status.jinja',
             status1=finalans, status=json.loads(status)
        )

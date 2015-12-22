"""
Web handler for beacon manager
"""
import base64
import json
import flask
import requests
from flask import Blueprint, render_template, flash, request
from oauth2client import client
from config import SCOPE, SUCCESS, ERROR
from beacons.portal.controller import controller
from beacons.portal.models import EddyStone, Header, IBeacon
from beacons.portal.models import Beacon
import beacons

portal = Blueprint('portal', __name__)
session = requests.Session()


@portal.route('/')
def list_beacons():
    """
    Returns list of registered beacons
    """
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
    """
    OAuth2.0 Callback
    """
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
    """
    Render template for register beacons
    """
    return render_template('register.jinja')


@portal.route('/register', methods=['POST'])
def register_beacons_status():
    """
    Return status of beacon registration
    """
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials']
    )
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        beacon = IBeacon(request.form)
        data = controller.register_beacon(beacon, credentials)
        name = controller.get_session_username(credentials)
        if data.get('error'):
            beacons.app.logger.warning(
                'USER: ' + name + '\nBeacon with ' + str(beacon) +
                ' failed to register.')
        else:
            beacons.app.logger.info(
                'USER: ' + name + '\nBeacon with ' + str(beacon) +
                ' registered successfully.')
        return render_template(
            'registration_status.jinja', status=data)


@portal.route('/unregister', methods=['GET'])
def unregister_beacons():
    """
    Render template to deactivate beacon
    """
    return render_template('unregister.jinja')


@portal.route('/unregister', methods=['POST'])
def unregister_beacons_status():
    """
    Returns status of deactivation of beacon
    """
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials']
    )
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        beacon = EddyStone(request.form)
        status = controller.deactivate_beacon(beacon, credentials)
        user = controller.get_session_username(credentials)
        beacons.app.logger.info(
            'USER: ' + user + '\nBeacon with ' + str(beacon) +
            ' unregistration successful.')
        return render_template(
            'unregistration_status.jinja', status=status
        )



@portal.route('/view', methods=['POST'])
def view_beacon():
    """
    Render template for edit beacon details
    """
    return render_template(
        'view.jinja', beacon=request.form.get('name'),
        advid=request.form.get('advid')
    )


@portal.route('/viewattach', methods=['POST'])
def list_beacons_attachment():
    """
    Returns status of deactivation of beacon
    """
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials']
    )
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        beacon = Beacon(request.form)
        status = controller.list_beacons_attachment(beacon, credentials)

        if ("attachments") in (json.loads(status)):
            decoded_message = base64.b64decode(
                (json.loads(status))['attachments'][0]['data']
            )
            attached_data = json.loads(decoded_message)
            return render_template('view_attachment.jinja',
                attachment=attached_data, status=json.loads(status))
        else:
            return render_template('view_attachment.jinja',
                msg="Sorry No Attachments Found")


@portal.route('/edit', methods=['POST'])
def edit_beacon():
    """
    Render template for edit beacon details
    """
    return render_template(
        'edit_beacon.jinja', beacon=request.form.get('name'),
        advid=request.form.get('advid')
    )


@portal.route('/edit-status', methods=['POST'])
def edit_beacon_status():
    """
    Returns the status of editing of beacon
    """
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials']
    )
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        beacon = EddyStone(request.form)
        user = controller.get_session_username(credentials)
        status = controller.modify_beacon(beacon, credentials)
        status = SUCCESS if status.get('beaconName') else ERROR
        if status == SUCCESS:
            beacons.app.logger.info(
                'USER:' + user + '\nModified beacon' + ' with ' + str(beacon) +
                'successfully.')
        else:
            beacons.app.logger.warning(
                'USER:' + user + '\nModified beacon' + ' with ' +
                str(beacon) + ' failed.')
        return render_template(
            'edit_beacon_status.jinja', status=status
        )


@portal.route('/attachment')
def attachment_beacons():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials']
    )

    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        beacon = Beacon(request.form)
        status = controller.namespace_of_beacon(beacon, credentials)

        data = status['namespaces'][0]['namespaceName']
        namespace = ((data.strip("namespaces")).replace('/', '')) + "/json"

    return render_template('attachment.jinja', beacon=namespace)


@portal.route('/attachment-status', methods=['POST'])
def beacon_attachment_status():
    """
    Returns the status of adding attachment to beacon
    """
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials']
    )

    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('portal.oauth2callback'))
    else:
        beacon = EddyStone(request.form)
        status = controller.attach_data_to_beacon(beacon, credentials)
        user = controller.get_session_username(credentials)
        try:
            json.loads(request.form['msg'])
            beacons.app.logger.info(
                'USER:' + user + '\nAdded attachement to' + ' beacon with ' +
                str(beacon) + ' successfully.')
        except ValueError:
            beacons.app.logger.error(
                'USER:' + user + '\nAdded attachement' + ' to beacon with ' +
                str(beacon) + ' raised valued error.')
            flash('Invalid Input !!!!')
            return flask.redirect(flask.url_for('portal.attachment_beacons'))

        decoded_message = base64.b64decode((json.loads(status))['data'])


        return render_template('attachment_status.jinja',
             attachment=attached_data, status=json.loads(status)
        )




@portal.route('/estimote-details', methods=['POST'])
def estimote_cloud_details():
    """
    Returns the details of the beacon available on estimote cloud
    """
    advertised_id = request.form.get('advid')
    beacon = controller.get_estimote_details(advertised_id)
    return render_template('estimote_details.jinja', beacon=beacon)


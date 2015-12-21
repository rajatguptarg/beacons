from flask import Blueprint, render_template, flash, request
import flask
import requests
from oauth2client import client
import json
import base64
from config import LIST_BEACONS, SCOPE, ATTACHMENT, SUCCESS, ERROR
from beacons.portal.controller import controller
from beacons.portal.models import Beacon, Header
import logging

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
        logging.info('Beacons are listed with OAuth Token - ' +
            credentials.access_token)
        header = Header(credentials.access_token)

        import pdb
        pdb.set_trace()

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
        logging.info('Beacon is registered with OAuth Token - ' +
            credentials.access_token)
        header = Header(credentials.access_token)
        auth_request = session.get(LIST_BEACONS,
            headers=header.get_header_body())

        return render_template(
            'beacons.jinja', beacons=json.loads(auth_request.content)
        )


@portal.route('/unregister', methods=['GET'])
def unregister_beacons():
    logging.info('Opened the Unregistration Form')
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
        logging.info('Beacon is unregistered with OAuth Token - ' +
            credentials.access_token)
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
        logging.info('Beacon is edited with OAuth Token - ' +
            credentials.access_token)
        beacon_details = Beacon(request.form)
        status = controller.modify_beacon(beacon_details, credentials)
        status = SUCCESS if status.get('beaconName') else ERROR
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
    logging.info('User wants to add attachemnts to beacons')
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

        try:
            json.loads(request.form['msg'])
        except ValueError:
            logging.info('Adding attachments raise ValueError Exception \
                with OAuth Token - ' + credentials.access_token)
            flash('Invalid Input !!!!')
            return flask.redirect(flask.url_for('portal.attachment_beacons'))

        logging.info('Adding attachments raise ValueError Exception \
            with OAuth Token - ' + credentials.access_token)

        ans = base64.b64decode((json.loads(status))['data'])
        finalans = json.loads(ans)
        return render_template(
            'attachment_status.jinja',
             status1=finalans, status=json.loads(status)
        )

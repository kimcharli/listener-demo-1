# We need to import request to access the details of the POST request
from flask import Flask, request
from flask.ext.restful import abort
import json
import os
from keystoneclient.auth.identity import v3
from keystoneclient import session
from novaclient import client as nova_client

# Openstack credentials
OPENSTACK_USERNAME = os.environ.get('OS_USERNAME')
OPENSTACK_PASSWORD = os.environ.get('OS_PASSWORD')
OPENSTACK_PROJECT_NAME = os.environ.get('OS_PROJECT_NAME')
OPENSTACK_USER_DOMAIN_NAME = os.environ.get('OS_USER_DOMAIN_NAME', 'default')
OPENSTACK_PROJECT_DOMAIN_NAME = \
    os.environ.get('OS_PROJECT_DOMAIN_NAME', 'default')
OPENSTACK_AUTH_URL = os.environ.get('OS_AUTH_URL')

# Configure auth and nova client
args = \
    {'AuthServerUrl': OPENSTACK_AUTH_URL,
     'OpenstackPassword': OPENSTACK_PASSWORD,
     'OpenstackProjectDomain': OPENSTACK_PROJECT_DOMAIN_NAME,
     'OpenstackTenant': OPENSTACK_PROJECT_NAME,
     'OpenstackUserDomain': OPENSTACK_USER_DOMAIN_NAME,
     'OpenstackUsername': OPENSTACK_USERNAME}

project_scoped_auth_plugin = v3.Password(
    auth_url=args['AuthServerUrl'],
    username=args['OpenstackUsername'],
    password=args['OpenstackPassword'],
    user_domain_name=args['OpenstackUserDomain'],
    project_name=args['OpenstackTenant'],
    project_domain_name=args['OpenstackProjectDomain'])

session = session.Session(auth=project_scoped_auth_plugin)
NOVA_CLIENT_VERSION = '2'
nova = nova_client.Client(NOVA_CLIENT_VERSION,
                          session=session,
                          endpoint_type='publicURL')

# Functions for migration
def get_instances(host):
    instances = \
        nova.servers.list(search_opts={'all_tenants': 1, 'host': host})
    return [instance.id for instance in instances]

def migrate_all_instances(host):
    instances = get_instances(host)
    for instance in instances:
        nova.servers.live_migrate(
            instance, None, True, False)

# Initialize the Flask application
app = Flask(__name__)

@app.route('/', methods=['POST'])
def app_message_post():
    message = "No action"
    try:
        if request.headers['Content-Type'] != 'application/json':
            return json.dumps({'result': message})
        data = request.json
        print("====\ndata posted: {}\n====".format(data))
        status = data['status']
        spec = data['spec']
        if spec['eventRuleId'] == 'Host_Risk_Transition':
            host = status['entityId']
            meta = status['metaData']
            if meta['new_state'] == 'at risk':
                migrate_all_instances(host)
                message = \
                    "Migrate all instances from Host {}".format(host)
        return json.dumps({'result': message})
    except Exception as e:
        abort(400, message="Hit an issue when processing message: {}"
                           .format(e))


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("7070")
    )

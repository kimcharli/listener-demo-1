from flask import Flask, request
from flask.ext.restful import abort
import json


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

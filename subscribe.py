# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json


# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a37qfp0ijxund6-ats.iot.eu-central-1.amazonaws.com"
CLIENT_ID = "testDevice"
PATH_TO_CERTIFICATE = "C:\\Users\\francesco\Desktop\\f92087215746c629910775eef89b5ee4e432ae31184fea604cb09644ca81aa80-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "C:\\Users\\francesco\Desktop\\f92087215746c629910775eef89b5ee4e432ae31184fea604cb09644ca81aa80-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "C:\\Users\\francesco\\Desktop\\AmazonRootCA1.pem"
MESSAGE = "Hello World"
TOPIC = "Tagliavini/Json/OvenRecipes/662352"
qos = mqtt.QoS.AT_MOST_ONCE
RANGE = 20
TIMEOUT = 30

# Define callback for incoming messages
def on_message_received(topic, payload, **kwargs):
    message = payload.decode('utf-8')
    print("Received message from topic '{}': {}".format(
        topic, payload.decode('utf-8')))
     # Parse incoming message as JSON
    try:
        data = json.loads(message)
    except json.JSONDecodeError as e:
        print("Failed to decode message as JSON: {}".format(str(e)))
        return

    # Extract relevant information from JSON
    recipe_id = data.get("recipe_id")
    temperature = data.get("temperature")
    duration = data.get("duration")

    # Do something with the extracted information
    print("Received recipe with ID {}, temperature {} and duration {}".format(
        recipe_id, temperature, duration))

# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )
print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))
# Make the connect() call
connect_future = mqtt_connection.connect()
# Future.result() waits until a result is available
connect_future.result()
print("Connected!")

#subscription:
print('Begin Subscription')
subscribe_future, packet_id = mqtt_connection.subscribe(
    topic=TOPIC,
    qos=mqtt.QoS.AT_MOST_ONCE,
    callback= on_message_received
)
# Wait for subscription to be acknowledged
suback_response = subscribe_future.result(TIMEOUT)
print("Subscribed with {}".format(str(suback_response['qos'])))

# Register callback with MQTT connection
mqtt_connection.on_message = on_message_received

# Wait for incoming messages
try:
    while True:
        t.sleep(0.1)
except KeyboardInterrupt:
    pass

disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()


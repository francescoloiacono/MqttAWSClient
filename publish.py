from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json


ENDPOINT = "a37qfp0ijxund6-ats.iot.eu-central-1.amazonaws.com"
CLIENT_ID = "testpublish"
PATH_TO_CERTIFICATE = "C:\\Users\\francesco\Desktop\\f92087215746c629910775eef89b5ee4e432ae31184fea604cb09644ca81aa80-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "C:\\Users\\francesco\Desktop\\f92087215746c629910775eef89b5ee4e432ae31184fea604cb09644ca81aa80-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "C:\\Users\\francesco\\Desktop\\AmazonRootCA1.pem"
MESSAGE = ""
TOPIC = "Tagliavini/Json/OvenRecipes/662352"
qos = mqtt.QoS.AT_LEAST_ONCE
RANGE = 20
TIMEOUT = 30

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
mqtt_connection.publish(topic=TOPIC, payload='', qos=mqtt.QoS.AT_LEAST_ONCE)
print("Published: '" + json.dumps(message) + "' to the topic: " + TOPIC)
    
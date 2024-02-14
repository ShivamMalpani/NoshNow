from confluent_kafka import Consumer
from user.user import RegistrationView
import os
import json


#Creating a consumer
consumer_conf = {
    'bootstrap.servers': 'localhost:9092', 
    'group.id': 'user-events-group',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(consumer_conf)
consumer.subscribe(['user-events']) 

#converting data into json format
def parse_event(event_data):
    event_info = json.loads(event_data)
    return event_info

#Handling the events in the queue
def process_event(event_data):
    event_info = parse_event(event_data)
    RegistrationView.send_otp_email(event_info["email"], event_info["otp"])

#A loop is run, to retrieve the messages polled by the consumer
try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Kafka Consumer Error: {msg.error()}")
            continue
        event_data = msg.value().decode('utf-8')
        process_event(event_data) 
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
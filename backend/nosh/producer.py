from confluent_kafka import Producer

#Creating the kafka producer
producer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'event-producer'
}
kafka_producer = Producer(producer_conf)
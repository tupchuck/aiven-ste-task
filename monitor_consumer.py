
import argparse
import os

from kafka import KafkaConsumer

from db import DBConnection


def consume_msgs(cert_folder="kafkaCerts/",
                 kafka_service_uri='hostname:1234',
                 db_service_uri='hostname:1234',
                 topic_name='monitoring'):

    consumer = KafkaConsumer(
      bootstrap_servers=kafka_service_uri,
      auto_offset_reset='earliest',
      security_protocol="SSL",
      ssl_cafile=cert_folder+"/ca.pem",
      ssl_certfile=cert_folder+"/service.cert",
      ssl_keyfile=cert_folder+"/service.key",
      consumer_timeout_ms=1000,
    )

    db = DBConnection(db_service_uri, topic_name)
    db.open()

    consumer.subscribe([topic_name])

    # Subscribe AND inject until stopped
    try:
        while True:
            for message in consumer:
                db.insert_message(message.value)
    except KeyboardInterrupt:
        print('Aborted!')

    # List all rows from DB
    # db.fetchAll()

    db.close()
    consumer.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--cert-folder',
        default=os.environ.get("KAFKA_CERT_FOLDER") or "kafkaCerts/",
        help="Path to folder containing required Kafka certificates"
    )
    parser.add_argument(
        '--kafka-service-uri',
        default=os.environ.get("KAFKA_SERVICE_URI"),
        help="Kafka Service URI (obtained from Aiven console)"
    )
    parser.add_argument(
        '--db-service-uri',
        default=os.environ.get("POSTGRES_SERVICE_URI"),
        help="PostgresSQL Service URI (obtained from Aiven console)"
    )
    parser.add_argument(
        '--topic-name',
        default=os.environ.get("KAFKA_TOPIC_NAME") or 'monitoring',
        help="Topic Name"
    )
    args = parser.parse_args()

    consume_msgs(cert_folder=args.cert_folder,
                 kafka_service_uri=args.kafka_service_uri,
                 db_service_uri=args.db_service_uri,
                 topic_name=args.topic_name)


if __name__ == "__main__":
    main()

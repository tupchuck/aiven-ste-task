
import argparse
import json
import os
import time

from kafka import KafkaProducer

from ping import ping


def produce_msgs(cert_folder="kafkaCerts/",
                 service_uri='hostname:1234',
                 topic_name='monitoring',
                 website_url='https://aiven.io',
                 max_requests=-1,
                 timeout=5):
    producer = KafkaProducer(
        bootstrap_servers=service_uri,
        security_protocol="SSL",
        ssl_cafile=cert_folder+"/ca.pem",
        ssl_certfile=cert_folder+"/service.cert",
        ssl_keyfile=cert_folder+"/service.key",
        value_serializer=lambda v: json.dumps(v).encode('ascii'),
        key_serializer=lambda v: json.dumps(v).encode('ascii')
    )

    if max_requests <= 0:
        max_requests = float('inf')
    i = 0
    try:
        while i < max_requests:
            message, key = ping(i, website_url)

            print("Sending: {}".format(message))
            # sending the message to Kafka
            producer.send(topic_name,
                          key=key,
                          value=message)
            # Sleeping time s
            print("Sleeping for..."+str(timeout)+'s')
            time.sleep(timeout)

            i = i + 1
    except KeyboardInterrupt:
        print('Aborted!')
    producer.flush()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--cert-folder',
        default=os.environ.get("KAFKA_CERT_FOLDER") or "kafkaCerts/",
        help="Path to folder containing required Kafka certificates"
    )
    parser.add_argument(
        '--service-uri',
        default=os.environ.get("KAFKA_SERVICE_URI"),
        help="Kafka Service URI (obtained from Aiven console)"
    )
    parser.add_argument(
        '--topic-name',
        default=os.environ.get("KAFKA_TOPIC_NAME") or 'monitoring',
        help="Topic Name"
    )
    parser.add_argument(
        '--website-url',
        default=os.environ.get("WEBSITE_MONITOR_URL") or 'https://aiven.io',
        help="Website URL to monitor"
    )
    parser.add_argument(
        '--max-requests',
        default=os.environ.get("WEBSITE_MONITOR_MAX_REQUESTS") or 5,
        help="Number of max requests (0 for unlimited)")
    parser.add_argument(
        '--timeout',
        default=os.environ.get("WEBSITE_MONITOR_REQUESTS_TIMEOUT") or 10,
        help="Timeout between requests in sec (0 for none)"
    )
    args = parser.parse_args()

    produce_msgs(cert_folder=args.cert_folder,
                 service_uri=args.service_uri,
                 topic_name=args.topic_name,
                 website_url=args.website_url,
                 max_requests=int(args.max_requests),
                 timeout=int(args.timeout))


if __name__ == "__main__":
    main()

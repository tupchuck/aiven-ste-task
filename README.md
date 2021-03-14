# Aiven Lead SET Homework

## Description

ℹ️ Note: this was initially forked and adopted from https://github.com/aiven/kafka-python-fake-data-producer

Also some of the examples from https://github.com/aiven/aiven-examples were used as a base material

## Task

Your task is to implement a system that monitors website availability over the network, produces metrics about this and passes these events through an Aiven Kafka instance into an Aiven PostgreSQL database.
For this, you need a Kafka producer which periodically checks the target websites and sends the check results to a Kafka topic, and a Kafka consumer storing the data to an Aiven PostgreSQL database. For practical reasons, these components may run in the same machine (or container or whatever system you choose), but in production use similar components would run in different systems.
The website checker should perform the checks periodically and collect the HTTP response time, error code returned, as well as optionally checking the returned page contents for a regexp pattern that is expected to be found on the page.

## Prerequisites

 * Apache Kafka
 * PostgreSQL

An Apache Kafka cluster can be created in minutes in any cloud of your choice using [Aiven.io console](https://console.aiven.io/signup).

## Installation

All required dependencies can be installed via

```bash
pip install -r requirements.txt
```

## Usage

### Producer

The Producer service can be run in bash with the following

```bash
python monitor_producer.py --cert-folder $KAFKA_CERT_FOLDER \
  --service-uri $KAFKA_SERVICE_URI \
  --topic-name $KAFKA_TOPIC_NAME \
  --max-requests 0 \
  --timeout 0 \
  --website-url https://aiven.io/
```

Where
* `cert-folder`: points to the folder containing the Kafka certificates
* `service-uri`: the Kafka Service URI
* `topic-name`: the Kafka topic name to write to (the topic needs to be pre-created or `kafka.auto_create_topics_enable` parameter enabled)
* `website-url`: the Website URL to monitor
* `max-requests`: the number of max requests during the session
* `timeout`: the timeout in seconds between requests

If successfully connected to a Kafka cluster, the command will start sending requests on the website url provided and output messages in a format

```json
{
  "id": 0,
  "status_code": 200,
  "response_time": 0.145518,
  "page_title": 'Aiven Database as a Service | Your data cloud',
}
```

With
* `id`: being the order number, starting from `0` until `max-requests`
* `status_code`: Status Code
* `response_time`: HTTP response time
* `page_title`: Title of the page requested

:exclamation: It will be running until `max-requests` number is reached or it's process interrupted (e.g. CTRL+C)

### Consumer

The Consumer service can be run in bash with the following

```bash
python monitor_consumer.py --cert-folder $KAFKA_CERT_FOLDER \
  --kafka-service-uri $KAFKA_SERVICE_URI \
  --db-service-uri $POSTGRES_SERVICE_URI
  --topic-name $KAFKA_TOPIC_NAME \
```

Where
* `cert-folder`: points to the folder containing the Kafka certificates
* `kafka-service-uri`: the Kafka Service URI
* `db-service-uri`: the PostgreSQL Service URI
* `topic-name`: the Kafka topic name to read from

:exclamation: It will be running until it's process interrupted (e.g. CTRL+C). You also can keep it running, if you want to execute producer for different websites. It will keep fetching data from subscribed topic.

## Testing

... TBD (just some simple tests were added 😞 ):

Run:

```bash
pytest
```

# Starting your Kafka Service with Aiven.io

If you don't have a Kafka Cluster available, you can easily start one in [Aiven.io console](https://console.aiven.io/signup).

Once created your account you can start your Kafka service with [Aiven.io's cli](https://github.com/aiven/aiven-client)

Set your variables first:
```bash
KAFKA_SERVICE_NAME=kafka-interview-task
PROJECT_NAME=my-project
CLOUD_REGION=aws-eu-south-1
AIVEN_PLAN_NAME=business-4
DESTINATION_FOLDER_NAME=~/kafkacerts
```
Parameters:
* `KAFKA_SERVICE_NAME`: the name you want to give to the Kafka instance
* `PROJECT_NAME`: the name of the project created during sing-up
* `CLOUD_REGION`: the name of the Cloud region where the instance will be created. The list of cloud regions can be found
 with
```bash
avn cloud list
```
* `AIVEN_PLAN_NAME`: name of Aiven's plan to use, which will drive the resources available, the list of plans can be found with
```bash
avn service plans --project <PROJECT_NAME> -t kafka --cloud <CLOUD_PROVIDER>
```
* `DESTINATION_FOLDER_NAME`: local folder where Kafka certificates will be stored (used to login)

You can create the Kafka service with

```bash
avn service create  \
  -t kafka $KAFKA_SERVICE_NAME \
  --project $PROJECT_NAME \
  --cloud  $CLOUD_PROVIDER \
  -p $AIVEN_PLAN_NAME \
  -c kafka_rest=true \
  -c kafka.auto_create_topics_enable=true \
  -c schema_registry=true
```

Use the Aiven Client to create a topic in your Kafka cluster:

```bash
avn service topic-create $KAFKA_SERVICE_NAME monitoring --partitions 3 --replication 3
```

---

You can download the required SSL certificates in the `<DESTINATION_FOLDER_NAME>` with

```bash
avn service user-creds-download $KAFKA_SERVICE_NAME \
  --project $PROJECT_NAME    \
  -d $DESTINATION_FOLDER_NAME \
  --username avnadmin
```

And retrieve the Kafka Service URI with

```bash
avn service get $KAFKA_SERVICE_NAME \
  --project $PROJECT_NAME \
  --format '{service_uri}'
```

The Kafka Service URI is in the form `hostname:port` and provides the `hostname` and `port` needed to execute the code.
You can wait for the newly created Kafka instance to be ready with

```bash
avn service wait $KAFKA_SERVICE_NAME --project $PROJECT_NAME
```

# Starting your PostgreSQL DB with Aiven.io

Launch a PostgreSQL service:

```bash
avn service create $POSTGRES_DB_NAME -t pg --plan hobbyist
```

And retrieve the PostgreSQL Service URI with

```bash
avn service get $POSTGRES_SERVICE_NAME \
  --project $PROJECT_NAME \
  --format '{service_uri}'
```

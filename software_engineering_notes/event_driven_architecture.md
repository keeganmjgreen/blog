# Event-Driven Architectures and Message Brokers

Event-Driven Architectures (EDAs) revolve around events:

- An **event**, **message**, or **record** represents the fact that something that happened, optionally with data related to what happened. An event should not describe which components publish or subscribe to such events or what they do with it.

- Events are **published / sent / written** and **subscribed to / received / read**.

- Each event is of a certain type, called a **topic**. An event of a certain type often follows a certain payload schema.

An EDA includes channels, operations, and components:

- An **event stream** or **channel** is like a queue for a certain type of event. An event stream is also referred to as a **topic**.

    A event stream is obviously analogous to the `chan` type in Go, except an EDA can span multiple processes (microservices, usually) across multiple machines.

- An **operation** is a process that causes an event to be sent (in which case the event's data may include the process's output) or is triggered when an event is received to do something useful with it.

    In the Go analogy, sending and receiving events is equivalent to `ch <- v` and `v := <-ch`, respectively, where an operation may be analogous to the code that executes before `ch <- v` or after `v := <-ch`.

- A **component** or **client** can send events to one or more topics (as an event **producer**), receive events from one or more topics (as an event **consumer**), or both.

    In the Go analogy, a component is equivalent to a goroutine.

For example, after receiving a request from a frontend, a user management microservice might publish an event to a `userSignedUp` topic including a user ID and email address. Another microservice subscribed to this topic might process this event by applying discount credits to the new user account for having signed up on a promotional day.

A topic can have any number of producers or consumers (including zero). For example, a zero-consumer EDA can be used solely for storing events.

A component can both publish and subscribe to the same topic.

Sending and waiting for an event is non-blocking. A producer does not wait for an event it has sent to be received or processed by a consumer, and a consumer can do other things while waiting to receive an event.

In an EDA, events are responded to immediately, which removes the need for polling and thus reduces both wait times and unnecessary computation. In an extreme example, if you did not use an EDA and had enough services polling the next one in a chain, their polling rates would accumulate into a longer wait time; an EDA avoids this.

## Kafka

[Apache Kafka](https://kafka.apache.org/) supports subscribing to, publishing, storing, real-time processing, and retroactive processing of events.

It follows a client-server architecture.

It is a distributed, scalable, elastic, fault-tolerant, and secure system consisting of a cluster of one or more servers:

- One or more of the servers, called **brokers**, form the "storage layer" which stores events.
- One or more of the servers run **Kafka Connect**.

Following the Kafka architecture, clients subscribe to, publish, and process events. REST APIs are available for this, as well as client libraries for languages including Go, Python, and more.

### Event storage

- A store of one topic's events is chronological and sometimes called a **log**.

- Storage durations can be configured per-topic.

- Topics are **partitioned**. An event is stored in one of its topic's partitions. The specific partition depends on the event's key. These partitions may be distributed across multiple brokers.

- Topics can be **replicated** across multiple brokers, potentially across datacenters or geo-regions. This ensures fault tolerance and high data availability (in case one broker server fails or needs maintenance).

### APIs

- The *Admin API* allows managing topics, brokers, etc.

- The *Producer API* allows publishing events.

- The *Consumer API* allows subscribing to / reading events.

- The *Kafka Streams API* allows transforming events from one or more topics into one or more other topics via operations such as aggregations, enrichments (analogous to joins in database terminology), windowing, and more.

- The *Kafka Connect API* allows transferring data to/from external systems (e.g., a relational database or another Kafka cluster) and the brokers.

### [Kafka Quickstart](https://kafka.apache.org/quickstart/)

Download Kafka:

```
wget https://dlcdn.apache.org/kafka/4.1.1/kafka_2.13-4.1.1.tgz
```

Extract and navigate within the downloaded zip folder:

```
tar -xzf kafka_2.13-4.1.1.tgz
cd kafka_2.13-4.1.1
```

Download the Kafka Docker image and run as a container:

```
docker pull apache/kafka:4.1.1
docker run -p 9092:9092 apache/kafka:4.1.1
```

Create a `quickstart-events` topic:

```
bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server localhost:9092
```

Get information about the topic:

```
bin/kafka-topics.sh --describe --topic quickstart-events --bootstrap-server localhost:9092
```

Write events to the topic:

```
bin/kafka-console-producer.sh --topic quickstart-events --bootstrap-server localhost:9092
```

Read events from the topic:

```
bin/kafka-console-consumer.sh --topic quickstart-events --from-beginning --bootstrap-server localhost:9092
```

Configure Kafka Connect to look in `connect-file-4.1.1.jar` for 
connector classes:
```
echo "plugin.path=libs/connect-file-4.1.1.jar" >> config/connect-standalone.properties
```

Create two lines of test data in `test.txt`:

```
echo -e "foo
bar" > test.txt
```

Start a standalone version of Kafka Connect, configured via the `config/
connect-standalone.properties` file and with two connectors (a `FileStreamSource` connector and a `FileStreamSink` connector):

```
bin/connect-standalone.sh config/connect-standalone.properties config/connect-file-source.properties config/connect-file-sink.properties
```

The `FileStreamSource` and `FileStreamSink` connectors are configured by the `config/connect-file-[source/sink].properties` files to read `test.txt` into the `connect-test` topic and write from that topic into `test.sink.txt`, respectively.

Verify that `FileStreamSource` successfully read events from `test.txt`:

```
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic connect-test --from-beginning
```

Verify that `FileStreamSink` successfully wrote the events to `test.sink.txt`:

```
more test.sink.txt
```

Clean up:

```
rm -rf /tmp/kafka-logs /tmp/kraft-combined-logs
```

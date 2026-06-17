from kafka import KafkaProducer, KafkaConsumer
import json
import os

BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

def get_producer() -> KafkaProducer:
    """Get Kafka producer with JSON serialization."""
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8") if k else None
    )

def get_consumer(topic: str, group_id: str) -> KafkaConsumer:
    """Get Kafka consumer for a given topic."""
    return KafkaConsumer(
        topic,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id=group_id,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True
    )

def publish_message(topic: str, key: str, value: dict):
    """Publish a message to a Kafka topic."""
    producer = get_producer()
    producer.send(topic, key=key, value=value)
    producer.flush()
    producer.close()

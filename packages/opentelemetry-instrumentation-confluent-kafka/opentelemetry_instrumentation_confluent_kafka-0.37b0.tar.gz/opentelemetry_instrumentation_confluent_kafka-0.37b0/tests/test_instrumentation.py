# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=no-name-in-module

from unittest import TestCase

from confluent_kafka import Consumer, Producer

from opentelemetry.instrumentation.confluent_kafka import (
    ConfluentKafkaInstrumentor,
    ProxiedConsumer,
    ProxiedProducer,
)


class TestConfluentKafka(TestCase):
    def test_instrument_api(self) -> None:
        instrumentation = ConfluentKafkaInstrumentor()

        producer = Producer({"bootstrap.servers": "localhost:29092"})
        producer = instrumentation.instrument_producer(producer)

        self.assertEqual(producer.__class__, ProxiedProducer)

        producer = instrumentation.uninstrument_producer(producer)
        self.assertEqual(producer.__class__, Producer)

        producer = Producer({"bootstrap.servers": "localhost:29092"})
        producer = instrumentation.instrument_producer(producer)

        self.assertEqual(producer.__class__, ProxiedProducer)

        producer = instrumentation.uninstrument_producer(producer)
        self.assertEqual(producer.__class__, Producer)

        consumer = Consumer(
            {
                "bootstrap.servers": "localhost:29092",
                "group.id": "mygroup",
                "auto.offset.reset": "earliest",
            }
        )

        consumer = instrumentation.instrument_consumer(consumer)
        self.assertEqual(consumer.__class__, ProxiedConsumer)

        consumer = instrumentation.uninstrument_consumer(consumer)
        self.assertEqual(consumer.__class__, Consumer)

    def test_consumer_commit_method_exists(self) -> None:
        instrumentation = ConfluentKafkaInstrumentor()

        consumer = Consumer(
            {
                "bootstrap.servers": "localhost:29092",
                "group.id": "mygroup",
                "auto.offset.reset": "earliest",
            }
        )

        consumer = instrumentation.instrument_consumer(consumer)
        self.assertEqual(consumer.__class__, ProxiedConsumer)
        self.assertTrue(hasattr(consumer, "commit"))

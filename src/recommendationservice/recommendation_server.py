#!/usr/bin/python
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Python
import os
import random
from typing import Iterable
import time
from concurrent import futures

# Pip
import grpc
from opentelemetry import trace

from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
    OTLPMetricExporter,
)
from opentelemetry.metrics import (
    CallbackOptions,
    Observation,
    get_meter_provider,
    # set_meter_provider,
)
# from opentelemetry.sdk.metrics import MeterProvider
# from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader


# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import (BatchSpanProcessor)
# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Local
import demo_pb2
import demo_pb2_grpc
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc
from logger import getJSONLogger

# from metrics import (
#     observable_counter_func,
#     observable_up_down_counter_func,
#     observable_gauge_func,
# )

# exporter = OTLPMetricExporter(insecure=True)
meter = get_meter_provider().get_meter(__name__)

## ---- Metrics
### ------- Metrics stuff
def observable_counter_func(options: CallbackOptions) -> Iterable[Observation]:
    yield Observation(1, {})


def observable_up_down_counter_func(
    options: CallbackOptions,
) -> Iterable[Observation]:
    yield Observation(-10, {})


def observable_gauge_func(options: CallbackOptions) -> Iterable[Observation]:
    yield Observation(9, {})


counter = meter.create_counter(
    name="requests_counter",
    description="number of requests",
    unit="1"
)
# counter.add(1)

# Async Counter
# observable_counter = meter.create_observable_counter(
#     "observable_counter",
#     [observable_counter_func],
# )

# UpDownCounter
updown_counter = meter.create_up_down_counter("updown_counter")
updown_counter.add(1)
updown_counter.add(-5)

# Async UpDownCounter
# observable_updown_counter = meter.create_observable_up_down_counter(
#     "observable_updown_counter", [observable_up_down_counter_func]
# )

# Histogram
histogram = meter.create_histogram(
    name="request_size_bytes",
    description="size of requests",
    unit="byte"
)    
# histogram = meter.create_histogram("histogram")
# histogram.record(99.9)

# Async Gauge
# gauge = meter.create_observable_gauge("gauge", [observable_gauge_func])

staging_attributes = {"environment": "staging"}


def set_metrics():

    print("Setting metrics")
    
    counter.add(random.randint(0, 25), staging_attributes)
    histogram.record(random.randint(0, 25), staging_attributes)
    updown_counter.add(random.randint(-5, 25), staging_attributes)

### ------- END Metrics stuff


class RecommendationService(demo_pb2_grpc.RecommendationServiceServicer):
    def ListRecommendations(self, request, context):
        prod_list = get_product_list(request.product_ids)
        span = trace.get_current_span()
        span.set_attribute("app.products_recommended.count", len(prod_list))
        logger.info("[Recv ListRecommendations] product_ids={}".format(prod_list))
        # build and return response
        response = demo_pb2.ListRecommendationsResponse()
        response.product_ids.extend(prod_list)
        return response

    def Check(self, request, context):
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.SERVING)

    def Watch(self, request, context):
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.UNIMPLEMENTED)


def get_product_list(request_product_ids):
    with tracer.start_as_current_span("get_product_list") as span:    
        set_metrics()
            
        max_responses = 5
        # fetch list of products from product catalog stub
        cat_response = product_catalog_stub.ListProducts(demo_pb2.Empty())        
        product_ids = [x.id for x in cat_response.products]
        span.set_attribute("app.products.count", len(product_ids))

        filtered_products = list(set(product_ids) - set(request_product_ids))
        num_products = len(filtered_products)
        span.set_attribute("app.filtered_products.count", num_products)

        num_return = min(max_responses, num_products)
        # sample list of indicies to return
        indices = random.sample(range(num_products), num_return)
        # fetch product ids from indices
        prod_list = [filtered_products[i] for i in indices]
        span.set_attribute("app.filtered_products.list", prod_list)
        return prod_list


def must_map_env(key: str):
    value = os.environ.get(key)
    if value is None:
        raise Exception(f'{key} environment variable must be set')
    return value

if __name__ == "__main__":
    logger = getJSONLogger('recommendationservice-server')
    tracer = trace.get_tracer_provider().get_tracer("recommendationservice")
    
    port = must_map_env('RECOMMENDATION_SERVICE_PORT')
    catalog_addr = must_map_env('PRODUCT_CATALOG_SERVICE_ADDR')
    
    channel = grpc.insecure_channel(catalog_addr)
    product_catalog_stub = demo_pb2_grpc.ProductCatalogServiceStub(channel)

    # create gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # add class to gRPC server
    service = RecommendationService()
    demo_pb2_grpc.add_RecommendationServiceServicer_to_server(service, server)
    health_pb2_grpc.add_HealthServicer_to_server(service, server)

    # start server
    logger.info("RecommendationService listening on port: " + port)
    server.add_insecure_port('[::]:' + port)
    server.start()
    server.wait_for_termination()
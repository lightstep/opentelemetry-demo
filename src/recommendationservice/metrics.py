#!/usr/bin/python

from typing import Iterable

from opentelemetry.metrics import (
    CallbackOptions,
    Observation,
    # get_meter_provider,
    # set_meter_provider,
)
# from opentelemetry.sdk.metrics import MeterProvider
# from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader


def observable_counter_func(options: CallbackOptions) -> Iterable[Observation]:
    yield Observation(1, {})


def observable_up_down_counter_func(
    options: CallbackOptions,
) -> Iterable[Observation]:
    yield Observation(-10, {})


def observable_gauge_func(options: CallbackOptions) -> Iterable[Observation]:
    yield Observation(9, {})

def init_metrics(meter):

    # Metrics init
    counter = meter.create_counter(
        name="requests_counter",
        description="number of requests",
        unit="1"
    )

    # Async Counter
    observable_counter = meter.create_observable_counter(
        "observable_counter",
        [observable_counter_func],
    )

    # UpDownCounter
    updown_counter = meter.create_up_down_counter("updown_counter")
    updown_counter.add(1)
    updown_counter.add(-5)

    # Async UpDownCounter
    observable_updown_counter = meter.create_observable_up_down_counter(
        "observable_updown_counter", [observable_up_down_counter_func]
    )

    # Histogram
    histogram = meter.create_histogram(
        name="request_size_bytes",
        description="size of requests",
        unit="byte"
    )    

    # Async Gauge
    gauge = meter.create_observable_gauge("gauge", [observable_gauge_func])

    staging_attributes = {"environment": "staging"}
    
    rs_metrics = {
        "counter": counter,
        "observable_counter": observable_counter,
        "updown_counter": updown_counter,
        "observable_updown_counter": observable_updown_counter,
        "histogram": histogram,
        "gauge": gauge,
        "staging_attributes": staging_attributes
    }
    
    return rs_metrics
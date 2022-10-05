#!/usr/bin/python

from gc import callbacks
from typing import Iterable
import psutil

from opentelemetry.metrics import (
    CallbackOptions,
    Observation,
)

# RAM usage
def get_ram_usage_callback(options: CallbackOptions) -> Iterable[Observation]:
    observations = []    
    ram_percent = psutil.virtual_memory().percent
    print(f"ram_percent: {ram_percent}")
    # add labels
    labels = {"dimension": "value"}
    observations.append(Observation(ram_percent, labels))
    # observer.observe(ram_percent, labels)
    
    return observations

# CPU usage
def get_cpu_usage_callback(options: CallbackOptions) -> Iterable[Observation]:
    observations = []    
    for (number, percent) in enumerate(psutil.cpu_percent(percpu=True)):
        print(f"cpu_number: {number}, cpu_percent: {percent}")
        labels = {"cpu_number": str(number)}
        observations.append(Observation(percent, labels))
        # observer.observe(percent, labels)
        
    return observations
        
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

    # CPU usage
    cpu_usage = meter.create_observable_up_down_counter(
        "cpu_percent",
        callbacks=[get_cpu_usage_callback],
        unit="%",
        description="per-CPU usage"
    )
    
    # RAM usage
    ram_usage = meter.create_observable_up_down_counter(
        "ram_usage",
        callbacks=[get_ram_usage_callback],
        unit="1",
        description="RAM usage"        
    )
    
    
    
    # meter.register_valueobserver(
    #     callback=get_cpu_usage_callback,
    #     name="cpu_percent",
    #     description="per-cpu usage",
    #     unit="1",
    #     value_type=float,
    # )

    staging_attributes = {"environment": "staging"}
    
    rs_metrics = {
        "counter": counter,
        "observable_counter": observable_counter,
        "updown_counter": updown_counter,
        "observable_updown_counter": observable_updown_counter,
        "histogram": histogram,
        "gauge": gauge,
        "staging_attributes": staging_attributes,
        "cpu_usage": cpu_usage,
        "ram_usage": ram_usage
    }
    
    return rs_metrics
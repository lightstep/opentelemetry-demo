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

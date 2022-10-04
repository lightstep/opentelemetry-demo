#!/bin/sh

opentelemetry-instrument \
  --traces_exporter console,otlp \
  --metrics_exporter console,otlp \
  --exporter_otlp_endpoint "http://otelcol:4317" \
  --exporter_otlp_insecure true \
  python recommendation_server.py

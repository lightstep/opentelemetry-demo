# Lightstep-Specific Information

In order to ease integration of upstream changes into this repository, please
avoid modifying upstream files. Eventually this can change.

## Usage

**Docker**: Run `docker compose -f <command>`

## Changes

- Collector config sends OTLP data to Lightstep via `otelcol-config-extras.yml`.
- Be sure to replace `<lightstep_access_token>` with your own [Lightstep access token](https://docs.lightstep.com/docs/create-and-manage-access-tokens#create-an-access-token).
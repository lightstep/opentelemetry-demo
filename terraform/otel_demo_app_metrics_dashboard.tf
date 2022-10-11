
resource "lightstep_metric_dashboard" "exported_dashboard" {
  project_name   = var.lightstep_project
  dashboard_name = "oTel Demo App - Application Metrics"

  chart {
    name = "Latency per Service"
    rank = "0"
    type = "timeseries"

    query {
      query_name          = "a"
      display             = "line"
      hidden              = false

      spans {
         query         = "service IN (\"adservice\", \"cartservice\", \"checkoutservice\", \"currencyservice\", \"emailservice\", \"featureflagservice\", \"frontend\", \"paymentservice\", \"productcatalogservice\", \"quoteservice\", \"recommendationservice\", \"shippingservice\")"
         operator      = "latency"
         group_by_keys = ["__component",]
         latency_percentiles = [50,95,99,99.9,]
      }

    }

  }

  chart {
    name = "Concurrent Requests"
    rank = "1"
    type = "timeseries"

    /* query {
      query_name          = "a"
      display             = "line"
      hidden              = false

      metric              = "app.products_recommended.request.count"
      timeseries_operator = "rate"


      group_by {
        aggregation_method = "sum"
        keys = []
      }

    } */
    query {
      query_name          = "a"
      display             = "line"
      hidden              = false

      tql                 =  <<EOT
      metric app.products_recommended.request.count | filter (instrumentation.name == "recommendationservice") | rate | group_by [], sum
      EOT
    }
  }

  chart {
    name = "CPU %"
    rank = "2"
    type = "timeseries"

    query {
      query_name          = "a"
      display             = "area"
      hidden              = false

      tql                 = "metric runtime.cpython.cpu_time | rate | group_by [], sum | point (value * 100)"

    }

  }

  chart {
    name = "Orders Placed"
    rank = "3"
    type = "timeseries"

    query {
      query_name          = "a"
      display             = "line"
      hidden              = false

      spans {
         query         = "operation IN (\"grpc.hipstershop.CheckoutService/PlaceOrder\")"
         operator      = "count"
         group_by_keys = []
      }

    }

  }

  chart {
    name = "/GetCart latency"
    rank = "4"
    type = "timeseries"

    query {
      query_name          = "a"
      display             = "line"
      hidden              = false

      spans {
         query         = "service IN (\"cartservice\") AND operation IN (\"hipstershop.CartService/GetCart\")"
         operator      = "latency"
         group_by_keys = ["__operation",]
         latency_percentiles = [50,95,99,99.9,]
      }

    }

  }

  chart {
    name = "/GetProduct latency"
    rank = "5"
    type = "timeseries"

    query {
      query_name          = "a"
      display             = "line"
      hidden              = false

      spans {
         query         = "service IN (\"productcatalogservice\") AND operation IN (\"hipstershop.ProductCatalogService/GetProduct\")"
         operator      = "latency"
         group_by_keys = ["__operation",]
         latency_percentiles = [50,95,99,99.9,]
      }

    }

  }

  chart {
    name = "Rate per Service"
    rank = "6"
    type = "timeseries"

    query {
      query_name          = "a"
      display             = "line"
      hidden              = false

      spans {
         query         = "service IN (\"adservice\", \"cartservice\", \"checkoutservice\", \"currencyservice\", \"emailservice\", \"featureflagservice\", \"frontend\", \"loadgenerator\", \"paymentservice\", \"productcatalogservice\", \"quoteservice\", \"recommendationservice\", \"shippingservice\")"
         operator      = "rate"
         group_by_keys = ["__component",]
      }

    }

  }

  chart {
    name = "Order Confirmations Sent"
    rank = "7"
    type = "timeseries"

    query {
      query_name          = "a"
      display             = "line"
      hidden              = false

      spans {
         query         = "operation IN (\"POST /send_order_confirmation\")"
         operator      = "count"
         group_by_keys = []
      }

    }

  }

  chart {
    name = "Ads count"
    rank = "8"
    type = "timeseries"

    query {
      query_name          = "a"
      display             = "line"
      hidden              = false

      spans {
         query         = "service IN (\"adservice\") AND \"app.ads.count\" IN (\"0\")"
         operator      = "count"
         group_by_keys = []
      }

    }

  }

  chart {
    name = "CartService/GetCart [Count]"
    rank = "9"
    type = "timeseries"

    query {
      query_name          = "a"
      display             = "line"
      hidden              = false

      spans {
         query         = "service IN (\"frontend\") AND operation IN (\"grpc.hipstershop.CartService/GetCart\", \"HTTP GET\", \"HTTP POST\")"
         operator      = "count"
         group_by_keys = []
      }

    }

  }

  chart {
    name = "otlp.exporter.seen"
    rank = "10"
    type = "timeseries"

    query {
      query_name          = "a"
      display             = "big_number"
      hidden              = false

      metric              = "otlp.exporter.seen"
      timeseries_operator = "delta"


      group_by {
        aggregation_method = "sum"
        keys = []
      }

    }

  }

  chart {
    name = "runtime.cpython.gc_count"
    rank = "11"
    type = "timeseries"

    query {
      query_name          = "a"
      display             = "line"
      hidden              = false

      metric              = "runtime.cpython.gc_count"
      timeseries_operator = "rate"


      group_by {
        aggregation_method = "sum"
        keys = []
      }

    }

  }

  chart {
    name = "runtime.cpython.memory"
    rank = "12"
    type = "timeseries"

    query {
      query_name          = "a"
      display             = "line"
      hidden              = false

      metric              = "runtime.cpython.memory"
      timeseries_operator = "rate"


      group_by {
        aggregation_method = "sum"
        keys = []
      }

    }

  }

}

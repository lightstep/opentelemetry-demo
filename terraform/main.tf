terraform {
  required_providers {
    lightstep = {
      source = "lightstep/lightstep"
      version = "~> 1.60.2"
    }
  }
  required_version = ">= v1.0.11"
}

 provider "lightstep" {
   api_key         = "<API>"
   organization    = "<ORG>"
 }


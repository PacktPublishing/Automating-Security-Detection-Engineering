# Terraform 0.13+ uses the Terraform Registry:

terraform {
#  backend "s3" {
#    bucket = "dc401-staging"
#    key    = "datadog-cloudsiem-tfstate"
#    region = "us-east-1"
#  }
  required_providers {
    datadog = {
      source = "DataDog/datadog"
    }
  }
}

variable "DD_API_KEY" {
  type        = string
  description = "Pull shell TF_VAR_DD_API_KEY" #e.g. export TF_VAR_API_KEY='apikeybar'
}

variable "DD_APP_KEY" {
  type        = string
  description = "Pull shell TF_VAR_DD_APP_KEY." #e.g. export TF_VAR_APP_KEY='appkeyfoo'
}

variable "DD_SITE" {
  type        = string
  description = "Pull shell TF_VAR_DD_SITE." #e.g. https://api.us5.datadoghq.com/
}

# Configure the Datadog provider
provider "datadog" {
  api_key = var.DD_API_KEY
  app_key = var.DD_APP_KEY
  api_url = var.DD_SITE
}

resource "datadog_security_monitoring_rule" "log4test" {
  name = "TEST-LOG4J"

  message = "This rule detects if your Apache or NGINX web servers are being scanned for the log4j vulnerability."
  enabled = false

  query {
    name        = "standard_attributes"
    query       = "source:(apache OR nginx) (@http.referer:(*jndi\\:ldap* OR *jndi\\:rmi* OR *jndi\\:dns*) OR @http.useragent:(*jndi\\:ldap* OR *jndi\\:rmi* OR *jndi\\:dns*))"
    aggregation = "count"
    #group_by_fields = ["host"]
  }

  case {
    name      = "standard attribute query triggered"
    status    = "info"
    condition = "standard_attributes > 0"
    #notifications = ["@user"]
  }

  options {
    evaluation_window   = 300
    keep_alive          = 3600
    max_signal_duration = 7200
  }

  tags = ["type:dos", "tactic:TA0043-reconnaissance", "security:attack"]
}

# Terraform 0.12- can be specified as:

# Configure the Datadog provider
# provider "datadog" {
#   api_key = "${var.datadog_api_key}"
#   app_key = "${var.datadog_app_key}"
# }
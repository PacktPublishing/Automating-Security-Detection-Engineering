terraform {
  required_providers {
    cloudflare = {
      source = "cloudflare/cloudflare"
      version = "4.20.0"
    }
  }
}


# Define null variables that are injected by terraform cloud
variable "CLOUDFLARE_API_TOKEN" {
  type= string
}
variable "CLOUDFLARE_EMAIL" {
  type = string
}
variable "CLOUDFLARE_ZONE_ID" {
  type = string
}


provider "cloudflare" {
  # Pull from tf cloud workspace level variables set to enviornment #
  #api_tokens are used but provider still expects api_key as of 2023-dec-22 commenting out for now
  #api_token = "${var.CLOUDFLARE_API_TOKEN}"
  #email = "${var.CLOUDFLARE_EMAIL}"

}

#New rule
#Syntax details https://registry.terraform.io/providers/cloudflare/cloudflare/latest/docs/resources/ruleset
resource "cloudflare_ruleset" "terraform_managed_resource_a93d3538be3d47c18220ae2d995a8a4b" {
  kind    = "zone"
  name    = "example test rule from dashboard"
  phase   = "http_request_firewall_custom"
  zone_id = "${var.CLOUDFLARE_ZONE_ID}"
  rules {
    action      = "managed_challenge"
    description = "test"
    enabled     = false
    expression  = "(http.request.method eq \"PATCH\" and http.referer eq \"google.com\")"
  }
}
/*
#additional rule
resource "cloudflare_ruleset" "zone_custom_firewall" {
  zone_id     = var.CLOUDFLARE_ZONE_ID
  name        = "prevent non web traffic on alt ports"
  description = "terraform update 1"
  kind        = "zone"
  phase       = "http_request_firewall_custom"

  rules {
    action = "managed_challenge"
    expression = "(not cf.edge.server_port in {80 443})"
    description = "Block ports other than 80 and 443"
    enabled = false
  }
}
*/

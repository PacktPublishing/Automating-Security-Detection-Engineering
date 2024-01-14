terraform {
  required_providers {
    wiz = {
      source  = "tf.app.wiz.io/wizsec/wiz"
      version = "~> 1.3"
    }
  }
}

resource "wiz_threat_detection_rule" "test" {
  name                    = "dennis-test_tdr"
  description             = "This is a test TDR"
  severity                = "LOW"
  target_event_names      = ["GuardDuty: UnauthorizedAccess:EC2/SSHBruteForce"]
  security_sub_categories = ["wsct-id-9468", "wsct-id-9469"]
  opa_matcher             = "match { input.RawEventName == 'UnauthorizedAccess:EC2/SSHBruteForce'; input.RawJson.Service.Archived == false }"
  cloud_providers         = ["AWS"]
  generate_findings       = false
  generate_issues         = false
}

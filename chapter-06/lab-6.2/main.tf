# Terraform 0.13+ uses the Terraform Registry:

terraform {
  backend "s3" {
    bucket = "<YOUR-BUCKET>"
    key    = "aws-eventbridge-rules-tfstate"
    region = "us-east-1"
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.32.1"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

### START EVENTBRIDGE RULES SECTION ###

resource "aws_cloudwatch_event_rule" "iamKeyCreated" {
  name           = "security-iam-access-key-generated"
  description    = "An IAM user has generated an long-term access key credential."
  event_bus_name = "default"
  state          = "ENABLED"
  tags = {
    Name        = "project" #tags must be in tf "map" format  as kv pairs
    Environment = "packt"
  }
  #user json encode function within tf to ensure proper parsing
  event_pattern = jsonencode(
    {
      "source" : ["aws.iam"],
      "detail-type" : ["AWS API Call via CloudTrail"],
      "detail" : {
        "eventSource" : ["iam.amazonaws.com"],
        "eventName" : ["CreateAccessKey"]
      }
    }
  )
}
#you must include a target as part of the rule or it wont do anything
resource "aws_cloudwatch_event_target" "sns" {
  rule      = aws_cloudwatch_event_rule.iamKeyCreated.name             #.name relates to the above resource
  target_id = "eventbridge-emailme"                                    #replace with your SNS topic
  arn       = "arn:aws:sns:us-east-1:<YOUR-ACCOUNT-INFO>:eventbridge-emailme" #replace with yours
}

### END RULE RESOURCE SECTION ####

/* 
#this is part of the example in the terraform provider documentation
#realistically you wouldnt have this in the rule because your
#states and stacks should be separate infrastructure, not rule management

resource "aws_sns_topic" "aws_logins" {
  name = "aws-console-logins"
}

resource "aws_sns_topic_policy" "default" {
  arn    = aws_sns_topic.aws_logins.arn
  policy = data.aws_iam_policy_document.sns_topic_policy.json
}

data "aws_iam_policy_document" "sns_topic_policy" {
  statement {
    effect  = "Allow"
    actions = ["SNS:Publish"]

    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }

    resources = [aws_sns_topic.aws_logins.arn]
  }
}
*/
provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "cloudtrail_logs" {
  bucket = var.bucket_name
}

resource "aws_cloudtrail" "trail" {
  name                          = "cloudhunter-trail"
  s3_bucket_name                = aws_s3_bucket.cloudtrail_logs.bucket
  include_global_service_events = true
  is_multi_region_trail         = true
  enable_logging                = true
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "cloudhunter-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_lambda_function" "detect_iam_abuse" {
  function_name = "detect_iam_abuse"
  runtime       = "python3.11"
  handler       = "detect_iam_abuse.lambda_handler"
  role          = aws_iam_role.lambda_exec_role.arn
  filename      = "../lambda/detect_iam_abuse.zip"
}

resource "aws_cloudwatch_event_rule" "every_15_min" {
  name                = "every-15-min"
  schedule_expression = "rate(15 minutes)"
}

resource "aws_cloudwatch_event_target" "lambda_trigger" {
  rule      = aws_cloudwatch_event_rule.every_15_min.name
  target_id = "CloudHunterTrigger"
  arn       = aws_lambda_function.detect_iam_abuse.arn
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.detect_iam_abuse.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_15_min.arn
}

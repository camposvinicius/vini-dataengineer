resource "aws_glue_catalog_database" "raw_vini" {
  name = "onboarding-a3-"
}

resource "aws_glue_crawler" "raw_vini" {
  database_name = aws_glue_catalog_database.raw_vini.name
  name          = "consumer-zone"
  role          = aws_iam_role.glue_role_vini.arn

  s3_target {
    path = "s3://${aws_s3_bucket.dl.bucket}/raw-data"
  }

  tags = {
    foo = "bar"
  }
}
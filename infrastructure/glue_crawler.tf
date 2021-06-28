resource "aws_glue_catalog_database" "TesteViniOnboardingRaw" {
  name = "onboarding-a3-"
}

resource "aws_glue_crawler" "raw" {
  database_name = aws_glue_catalog_database.TesteViniOnboardingRaw.name
  name          = "consumer-zone"
  role          = aws_iam_role.glue_role.arn

  s3_target {
    path = "s3://${aws_s3_bucket.dl.bucket}/raw-data/titanic"
  }

  configuration = <<EOF
{
   "Version": 1.0,
   "Grouping": {
      "TableGroupingPolicy": "CombineCompatibleSchemas" }
}
EOF

  tags = {
    foo = "bar"
  }
}
#
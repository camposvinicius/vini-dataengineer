resource "aws_ecr_repository" "repo-vini" {
  name                 = "etl-job-vini"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
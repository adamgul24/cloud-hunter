terraform {
  backend "s3" {
    bucket = "cloudhunter-tf-backend"
    key    = "terraform.tfstate"
    region = "us-east-1"
    dynamodb_table = "cloudhunter-locks"
  }
}

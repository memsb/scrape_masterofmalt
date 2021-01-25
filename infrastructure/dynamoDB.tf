provider "aws" {
  profile = "default"
  region = "eu-west-2"
}

resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name = "master_of_malt"
  billing_mode = "PAY_PER_REQUEST"
  hash_key = "date"

  attribute {
    name = "date"
    type = "S"
  }

  ttl {
    attribute_name = "TimeToExist"
    enabled = false
  }

  tags = {
    Name = "scan_mom"
    Environment = "production"
  }
}

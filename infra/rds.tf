resource "aws_dynamodb_table" "messages_table" {
  name           = "messages"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "text"
    type = "S"
  }

  attribute {
    name = "message_attributes"
    type = "S"
  }

  global_secondary_index {
    name            = "text-index"
    hash_key        = "text"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "message-attributes-index"
    hash_key        = "message_attributes"
    projection_type = "ALL"
  }

  tags = {
    Environment = "dev"
    Name        = "messages-table"
  }
}
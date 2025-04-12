# Cria uma chave kms para criptografar as mensagens
resource "aws_kms_key" "kms_key" {
  description             = "Chave KMS para criptografar as mensagens do SNS e do SQS"
  deletion_window_in_days = 10
}
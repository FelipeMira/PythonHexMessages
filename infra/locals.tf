# Criar algumas variáveis locais para os nomes do SQS e do SNS
locals {
  sqs-receive-name = "sqs-receive-env-${var.env-name}"
  sqs-alerts-name = "sqs-alerts-env-${var.env-name}"
  sqs-errors-name = "sqs-errors-env-${var.env-name}"
  sns-name = "sns-receive-env-${var.env-name}"
}

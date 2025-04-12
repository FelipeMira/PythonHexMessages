# Declarar a variável env-name, que representa o nome do ambiente
variable "env-name" {
  type        = string
  default     = "dev"
  description = "O nome do ambiente (dev, prod, etc.)"
}

# Declarar a variável region, que representa a região da AWS
variable "region" {
  type        = string
  default     = "sa-east-1"
  description = "A região da AWS onde os recursos serão criados"
}

# Define o nome da chave KMS
variable "kms_key_name" {
  type        = string
  default     = "kms-key"
  description = "Nome da chave KMS para criptografar as mensagens do SNS e do SQS"
}

# Define o nome do tópico SNS
variable "sns_topic_name" {
  type        = string
  default     = "sns-receive"
  description = "Nome do tópico SNS para publicar as mensagens"
}

# Define o nome do tópico SQS
variable "sqs_queue_name" {
  type        = string
  default     = "sqs-queue"
  description = "Nome do tópico SQS para receber as mensagens"
}

# Define o nome do filtro para a inscrição do SQS no SNS
variable "filter_name" {
  type        = string
  default     = "x-type"
  description = "Nome do atributo da mensagem que será usado como filtro"
}

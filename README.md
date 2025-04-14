# Projeto: Sistema de Processamento de Mensagens com SQS e DynamoDB

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![AWS](https://img.shields.io/badge/aws-localstack-orange.svg)](https://localstack.cloud/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Descrição do Projeto

Este projeto é uma aplicação desenvolvida em Python para processar mensagens recebidas de filas **AWS SQS** ou via **AWS Lambda**. Ele utiliza uma arquitetura baseada em portas e adaptadores (Ports and Adapters ou Hexagonal Architecture), promovendo a separação de responsabilidades e facilitando a manutenção e extensibilidade do sistema.

O sistema é responsável por:
- Receber mensagens de uma fila SQS ou via request de um API Gateway para um Lambda.
- Processar as mensagens de acordo com regras de negócio.
- Enviar mensagens processadas para filas de saída (alerta ou erro).
- Gerenciar o reconhecimento (acknowledgment) das mensagens.
- Tratar erros de forma centralizada utilizando o `GlobalExceptionHandler`.

---

## Estrutura do Projeto

A estrutura do projeto segue os princípios da arquitetura hexagonal, dividindo o código em camadas bem definidas:

### 1. **Adapters (Adaptadores)**
Responsáveis por conectar o sistema com o mundo externo, como filas SQS, Lambda e mapeamento de mensagens.

- **Inbound Adapters**: Recebem mensagens de entrada.
  - `app/src/adapters/inbound/message/sqs/sqs_input_adapter.py`: Escuta mensagens da fila SQS e as processa.
  - `app/src/adapters/inbound/serverless/awslambda/lambda_handler.py`: Recebe eventos de entrada via AWS Lambda.

- **Outbound Adapters**: Enviam mensagens para filas de saída.
  - `app/src/adapters/outbound/message/sqs/sqs_output_alert.py`: Envia mensagens de alerta para a fila SQS.
  - `app/src/adapters/outbound/message/sqs/sqs_output_error.py`: Envia mensagens de erro para a fila SQS.
  - `app/src/adapters/outbound/database/dynamo/dynamo_db_persistor.py`: Persistência de mensagens em um banco de dados DynamoDB.

### 2. **Application (Regras de Negócio)**
Contém os casos de uso e serviços que implementam as regras de negócio.

- `app/src/application/ports/inbound/process_message_use_case.py`: Define a interface para o processamento de mensagens.
- `app/src/application/ports/outbound/send_message.py`: Define a interface para envio de mensagens.
- `app/src/application/ports/outbound/persist_message.py`: Define a interface para persistência de mensagens.
- `app/src/application/services/process_message_service.py`: Implementa o caso de uso de processamento de mensagens.

### 3. **Domain (Domínio)**
Representa o núcleo do sistema, contendo as entidades e regras de negócio puras.

- `app/src/application/domain/message.py`: Define o modelo de domínio para mensagens.

### 4. **Common (Utilitários e Configurações)**
Contém configurações e utilitários compartilhados.

- `app/src/common/properties_env.py`: Gerencia variáveis de ambiente.
- `app/src/common/log_config.py`: Configura o logger para exibir logs no formato JSON.

### 5. **Serverless Errors (Tratamento de Erros)**
Gerencia o tratamento centralizado de erros usando o padrão **Strategy**.

- `app/src/adapters/inbound/serverless/errors/global_exception_handler.py`: Gerencia o tratamento centralizado de erros.
- `app/src/adapters/inbound/serverless/errors/exception_handler_strategy.py`: Define a interface para estratégias de tratamento de erros.
- `app/src/adapters/inbound/serverless/errors/key_error_exception.py`: Trata erros do tipo `KeyError`.
- `app/src/adapters/inbound/serverless/errors/value_error_exception.py`: Trata erros do tipo `ValueError`.
- `app/src/adapters/inbound/serverless/errors/business_exception_handler.py`: Trata erros de negócio.
- `app/src/adapters/inbound/serverless/errors/default_exception_handler.py`: Trata erros genéricos.

### 6. **Configuration (Inicialização)**
Gerencia a inicialização do sistema.

- `app/src/configuration/application.py`: Configura e inicia o sistema.
- `app/src/configuration/main.py`: Ponto de entrada principal da aplicação.

---

## Padrões Utilizados

### 1. **Arquitetura Hexagonal**
- Promove a separação entre lógica de negócio e detalhes de implementação.
- Facilita a substituição de tecnologias externas (ex.: troca de SQS por outro sistema de mensageria).

### 2. **Singleton**
- Utilizado para garantir que certas classes (ex.: `SqsConfig`) tenham apenas uma instância durante a execução.

### 3. **Mapper**
- Utilizado para converter mensagens entre diferentes formatos (ex.: AWS SQS para o modelo de domínio).

### 4. **Dependency Injection**
- As dependências são injetadas nas classes, facilitando testes e promovendo baixo acoplamento.

### 5. **Interface Segregation**
- Interfaces como `ProcessMessage` e `SendMessage` garantem que as implementações sigam contratos bem definidos.

---

## Tecnologias Utilizadas

- **Python**: Linguagem principal.
- **AWS SQS**: Serviço de filas para comunicação assíncrona.
- **boto3**: SDK para integração com AWS.
- **python-dotenv**: Gerenciamento de variáveis de ambiente.
- **python-json-logger**: Formatação de logs em JSON.
- **AWS DynamoDB**: Banco de dados NoSQL para persistência de mensagens.

---

## Configuração do Ambiente

#### Localstack padrão:
- Execute o comando:
```shell
cd docker && docker-compose up
``` 
- Se tudo ocorreu bem seu ambiente está configurado.

#### Executando criação da infraestrutura

- Devemos ir até a pasta de infraestrutura e executar o comando:
```shell
terraform -chdir=./infra init && terraform -chdir=./infra plan && terraform -chdir=./infra apply -auto-approve
```

#### Configurar o arquivo de credenciais da aws

- Dentro da pasta `~/.aws/` crie um arquivo chamado `credentials` e adicione o seguinte conteúdo:
- Substitua os valores de `aws_access_key_id` e `aws_secret_access_key` pelos valores que estão no arquivo `docker-compose.yml`:

```text
[localstack]
aws_access_key_id = test
aws_secret_access_key = test
```

#### Configurar o arquivo de config da aws

- Dentro da pasta `~/.aws/` crie um arquivo chamado `config` e adicione o seguinte conteúdo:
- Substitua o valor de `region` pelo valor que está no arquivo `docker-compose.yml`:

```text
[profile localstack]
region=sa-east-1
output=json
endpoint_url=http://localhost:4566
[default]
region = sa-east-1
output = json
```


1. **Instalar Dependências**:
   ```bash
   pip install -r src/requirements.txt
   ```

2. **Configurar Variáveis de Ambiente**:
   - Crie arquivos `.env` no diretório `configuration/resources` para cada ambiente (ex.: `.env.local`, `.env.prod`).
   - Exemplo de variáveis:
     ```
     QUEUE_URL=https://sqs.sa-east-1.amazonaws.com/123456789012/queue
     QUEUE_URL_ERROR=https://sqs.sa-east-1.amazonaws.com/123456789012/error-queue
     QUEUE_URL_ALERT=https://sqs.sa-east-1.amazonaws.com/123456789012/alert-queue
     AWS_SQS_OUT_QUEUES_ERROR_X_TYPE=error
     AWS_SQS_OUT_QUEUES_ALERT_X_TYPE=alert
     DYNAMODB_TABLE_NAME=messages
     ```

---

## Logs

Os logs são configurados para exibir mensagens no formato JSON com codificação UTF-8. Exemplo de log:
```json
{
  "timestamp": "2023-10-01T12:00:00",
  "name": "root",
  "levelname": "INFO",
  "message": "Mensagem processada com sucesso",
  "filename": "sqs_input_adapter.py",
  "funcName": "listen_to_sqs_queue",
  "lineno": 42
}
```

---

## Testes

- **Testes Unitários**: Devem ser implementados para cada camada, garantindo a cobertura de casos de uso e adaptadores.
- **Mock de SQS**: Utilize bibliotecas como `moto` para simular o comportamento do SQS em testes.

---

## Como enviar mensagens ao tópico sns?

#### Mensagem para fila de alerta

```shell
aws sns publish --topic-arn "arn:aws:sns:sa-east-1:000000000000:sns-receive-env-dev" \
--message '{"default": "Mensagem de teste"}' \
--message-structure json \
--message-attributes '{"x-type":{"DataType":"String","StringValue":"alert"}, "x-queueUrl":{"DataType":"String","StringValue":"alert"}}' \
--endpoint-url=http://localhost:4566 \
--profile=localstack
```

#### Mensagem para fila de erro

```shell
aws sns publish \
 --topic-arn "arn:aws:sns:sa-east-1:000000000000:sns-receive-env-dev" \
 --message="Mensagem de teste" \
 --message-attributes '{"x-type":{"DataType":"String","StringValue":"error"}, "x-queueUrl":{"DataType":"String","StringValue":"error"}}' \
 --endpoint-url=http://localhost:4566 \
 --profile=localstack
```

## Projeto consumidor da fila SQS

- Foi criado um projeto que consome da fila sqs e envia a mensagem para outra fila.
- Vamos enviar uma mensagem na fila `sqs-receive-env-dev` recepcionar no fluxo de entrada e enviar para a fila `sqs-alerts-env-dev`.
- Após o primeiro teste vamos enviar uma mensagem na fila `sqs-receive-env-dev` recepcionar no fluxo de entrada e enviar para a fila `sqs-error-env-dev`.
- Para direcionar para a fila correta utilizamos o padrão Strategy. No padrão Strategy, um comportamento ou algoritmo 
é encapsulado em uma classe, e a classe cliente pode escolher o algoritmo apropriado em tempo de execução. 
No nosso caso, a interface SendMessage define um comportamento comum (enviar uma mensagem), e as classes SQSOutputAlert 
e SQSOutputError implementam esse comportamento de maneiras diferentes. A classe ProcessMessageService pode então 
escolher qual estratégia usar com base no tipo de mensagem.

#### Mensagem para fila de recebimento e enviando para a fila de alerta

```shell
aws sqs send-message --queue-url "http://localhost:4566/000000000000/sqs-receive-env-dev" \
--message-body '{"default": "Mensagem de teste"}' \
--message-attributes '{"x-type":{"DataType":"String","StringValue":"alert"}, "x-queueUrl":{"DataType":"String","StringValue":"alert"}}' \
--endpoint-url=http://localhost:4566 \
--profile=localstack
```

#### Mensagem para fila de recebimento e enviando para a fila de erros

```shell
aws sqs send-message --queue-url "http://localhost:4566/000000000000/sqs-receive-env-dev" \
--message-body '{"default": "Mensagem de teste"}' \
--message-attributes '{"x-type":{"DataType":"String","StringValue":"error"}, "x-queueUrl":{"DataType":"String","StringValue":"error"}}' \
--endpoint-url=http://localhost:4566 \
--profile=localstack
```## Como enviar mensagens ao tópico sns?

#### Configurar o arquivo de credenciais da aws

- Dentro da pasta `~/.aws/` crie um arquivo chamado `credentials` e adicione o seguinte conteúdo:
- Substitua os valores de `aws_access_key_id` e `aws_secret_access_key` pelos valores que estão no arquivo `docker-compose.yml`:

```text
[localstack]
aws_access_key_id=teste
aws_secret=teste
```

#### Configurar o arquivo de config da aws

- Dentro da pasta `~/.aws/` crie um arquivo chamado `config` e adicione o seguinte conteúdo:
- Substitua o valor de `region` pelo valor que está no arquivo `docker-compose.yml`:

```text
[profile localstack]
region=sa-east-1
output=json
endpoint_url=http://localhost:4566
[default]
region = sa-east-1
output = json
```

#### Mensagem para fila de alerta

```shell
aws sns publish --topic-arn "arn:aws:sns:sa-east-1:000000000000:sns-receive-env-dev" \
--message '{"default": "Mensagem de teste"}' \
--message-structure json \
--message-attributes '{"x-type":{"DataType":"String","StringValue":"alert"}, "x-queueUrl":{"DataType":"String","StringValue":"alert"}}' \
--endpoint-url=http://localhost:4566 \
--profile=localstack
```

#### Mensagem para fila de erro

```shell
aws sns publish \
 --topic-arn "arn:aws:sns:sa-east-1:000000000000:sns-receive-env-dev" \
 --message="Mensagem de teste" \
 --message-attributes '{"x-type":{"DataType":"String","StringValue":"error"}, "x-queueUrl":{"DataType":"String","StringValue":"error"}}' \
 --endpoint-url=http://localhost:4566 \
 --profile=localstack
```

## Projeto consumidor da fila SQS

- Foi criado um projeto que consome da fila sqs e envia a mensagem para outra fila.
- Vamos enviar uma mensagem na fila `sqs-receive-env-dev` recepcionar no fluxo de entrada e enviar para a fila `sqs-alerts-env-dev`.
- Após o primeiro teste vamos enviar uma mensagem na fila `sqs-receive-env-dev` recepcionar no fluxo de entrada e enviar para a fila `sqs-error-env-dev`.
- Para direcionar para a fila correta utilizamos o padrão Strategy. No padrão Strategy, um comportamento ou algoritmo 
é encapsulado em uma classe, e a classe cliente pode escolher o algoritmo apropriado em tempo de execução. 
No nosso caso, a interface SendMessage define um comportamento comum (enviar uma mensagem), e as classes SQSOutputAlert 
e SQSOutputError implementam esse comportamento de maneiras diferentes. A classe ProcessMessageService pode então 
escolher qual estratégia usar com base no tipo de mensagem.

#### Executando o projeto

- Se quisermos utilizar como um listener devemos alterar o main.py:
```python
if __name__ == "__main__":
    #Application.lambda_handler(event, context)
    Application.start()
```

- Se quisermos utilizar como um lambda handler devemos alterar o main.py:
```python
if __name__ == "__main__":
    Application.lambda_handler(event, context)
    #Application.start()
```

- Devemos executar o comando: 
```shell
python src/configuration/main.py
```

#### Mensagem para fila de recebimento e enviando para a fila de alerta

```shell
aws sqs send-message --queue-url "http://localhost:4566/000000000000/sqs-receive-env-dev" \
--message-body '{"default": "Mensagem de teste"}' \
--message-attributes '{"x-type":{"DataType":"String","StringValue":"alert"}, "x-queueUrl":{"DataType":"String","StringValue":"alert"}}' \
--endpoint-url=http://localhost:4566 \
--profile=localstack
```

#### Mensagem para fila de recebimento e enviando para a fila de erros

```shell
aws sqs send-message --queue-url "http://localhost:4566/000000000000/sqs-receive-env-dev" \
--message-body '{"default": "Mensagem de teste"}' \
--message-attributes '{"x-type":{"DataType":"String","StringValue":"error"}, "x-queueUrl":{"DataType":"String","StringValue":"error"}}' \
--endpoint-url=http://localhost:4566 \
--profile=localstack
```

## Contribuição

1. Faça um fork do repositório.
2. Crie uma branch para sua feature/bugfix:
   ```bash
   git checkout -b minha-feature
   ```
3. Envie suas alterações:
   ```bash
   git commit -m "Descrição da alteração"
   git push origin minha-feature
   ```
4. Abra um Pull Request.

---

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
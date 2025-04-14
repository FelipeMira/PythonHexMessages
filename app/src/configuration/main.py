from app.src.configuration.application import Application

# Exemplo de evento para teste do lambda_handler
event = {
    "version": "2.0",
    "routeKey": "POST /message",
    "rawPath": "/message",
    "rawQueryString": "parameter1=value1&parameter1=value2&parameter2=value",
    "cookies": [
        "cookie1",
        "cookie2"
    ],
    "headers": {
        "content-type": "application/json",
        "x-type": "alert"
    },
    "queryStringParameters": {
        "parameter1": "value1,value2",
        "parameter2": "value"
    },
    "requestContext": {
        "accountId": "123456789012",
        "apiId": "api-id",
        "authentication": {
            "clientCert": {
                "clientCertPem": "CERT_CONTENT",
                "subjectDN": "www.example.com",
                "issuerDN": "Example issuer",
                "serialNumber": "a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1",
                "validity": {
                    "notBefore": "May 28 12:30:02 2019 GMT",
                    "notAfter": "Aug  5 09:36:04 2021 GMT"
                }
            }
        },
        "authorizer": {
            "jwt": {
                "claims": {
                    "claim1": "value1",
                    "claim2": "value2"
                },
                "scopes": [
                    "scope1",
                    "scope2"
                ]
            }
        },
        "domainName": "id.execute-api.sa-east-1.amazonaws.com",
        "domainPrefix": "id",
        "http": {
            "method": "POST",
            "path": "/message",
            "protocol": "HTTP/1.1",
            "sourceIp": "192.168.0.1/32",
            "userAgent": "agent"
        },
        "requestId": "id",
        "routeKey": "$default",
        "stage": "$default",
        "time": "12/Mar/2020:19:03:58 +0000",
        "timeEpoch": 1583348638390
    },
    "body": "{\"default\": \"messagem padrao\"}",
    "pathParameters": {
        "parameter1": "value1"
    },
    "isBase64Encoded": 'true',
    "stageVariables": {
        "stageVariable1": "value1",
        "stageVariable2": "value2"
    }
}

# Contexto fictício para teste
context = {}

if __name__ == "__main__":
    Application.lambda_handler(event, context)
    #Application.start()
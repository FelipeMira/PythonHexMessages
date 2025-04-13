class Response:
    def __init__(self, status_code: int, body: str, headers: list = None, cookies: list = None, is_base64_encoded: bool = False, method: str = None):
        """
        Inicializa uma resposta com código de status, corpo, cabeçalhos e cookies.

        :param status_code: Código de status HTTP.
        :param body: Corpo da resposta.
        :param headers: Lista de tuplas representando os cabeçalhos HTTP.
        :param cookies: Lista de cookies.
        :param is_base64_encoded: Indica se o corpo está codificado em Base64.
        :param method: Método HTTP chamado.
        """
        self.status_code = status_code
        self.body = body
        self.headers = {key: value for key, value in (headers or [])}
        if method:
            self.headers["X-Method-Called"] = method
        self.cookies = cookies or []
        self.is_base64_encoded = is_base64_encoded

    def to_dict(self):
        """
        Converte a resposta para o formato esperado por uma AWS Lambda.

        :return: Dicionário no formato esperado.
        """
        return {
            "statusCode": self.status_code,
            "body": self.body,
            "headers": self.headers,
            "cookies": self.cookies,
            "isBase64Encoded": self.is_base64_encoded,
        }
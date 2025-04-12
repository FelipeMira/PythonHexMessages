class BusinessException(Exception):
    def __init__(self, message=None, errors=None):
        """
        Construtor com argumentos opcionais (no args constructor).
        :param message: Mensagem de erro.
        :param errors: Dicionário contendo detalhes adicionais sobre os erros.
        """
        super().__init__(message)
        self._message = message
        self._errors = errors or {}

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value: str):
        self._message = value

    @property
    def errors(self):
        return self._errors

    @errors.setter
    def errors(self, value: dict):
        self._errors = value

    @classmethod
    def builder(cls):
        """
        Retorna uma instância do Builder para criar objetos BusinessException.
        """
        return cls.BusinessExceptionBuilder()

    class BusinessExceptionBuilder:
        def __init__(self):
            self._message = None
            self._errors = {}

        def with_message(self, message: str):
            self._message = message
            return self

        def with_errors(self, errors: dict):
            self._errors = errors
            return self

        def build(self):
            return BusinessException(self._message, self._errors)

    def __str__(self):
        return f"BusinessException(message={self.message}, errors={self.errors})"
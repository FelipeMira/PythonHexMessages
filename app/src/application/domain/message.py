class Message:
    def __init__(self, message_attributes=None, text=None):
        """
        Construtor com argumentos opcionais (no args constructor).
        :param message_attributes: Dicionário contendo os atributos da mensagem.
        :param text: Texto da mensagem.
        """
        self._message_attributes = message_attributes or {}
        self._text = text

    @property
    def message_attributes(self):
        return self._message_attributes

    @message_attributes.setter
    def message_attributes(self, value: dict[str, str]):
        self._message_attributes = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value

    @classmethod
    def builder(cls):
        """
        Retorna uma instância do Builder para criar objetos Message.
        """
        return cls.MessageBuilder()

    class MessageBuilder:
        def __init__(self):
            self._message_attributes = {}
            self._text = ""

        def with_message_attributes(self, message_attributes: dict[str, str]):
            self._message_attributes = message_attributes
            return self

        def with_text(self, text: str):
            self._text = text
            return self

        def build(self):
            return Message(self._message_attributes, self._text)

    def __repr__(self):
        return f"Message(message_attributes={self.message_attributes}, text={self.text})"
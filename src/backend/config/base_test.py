from src.backend.services.chat_api import ChatAPI


class BaseTest:

    def setup_method(self):
        self.chat_api = ChatAPI()

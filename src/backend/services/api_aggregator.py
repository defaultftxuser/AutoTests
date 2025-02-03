from src.backend.services.chat_api import ChatAPI


class APIAggregator:

    def __init__(self):
        self.chat_api = ChatAPI()

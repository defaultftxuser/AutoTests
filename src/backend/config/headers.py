from faker import Faker


class Headers:

    @staticmethod
    def get_chat_headers(session_id):
        return {
            "Session-Id": f"{session_id}",
        }

    @staticmethod
    def get_chat_header_value() -> str:
        return Faker().uuid4()

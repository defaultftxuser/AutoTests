

class Headers:

    @staticmethod
    def get_chat_headers(session_id: str) -> dict[str, str]:
        return {
            "Session-Id": f"{session_id}",
        }

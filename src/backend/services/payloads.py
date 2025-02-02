import json
from typing import Any, Optional
from faker import Faker

fake = Faker()


class Payloads:

    @staticmethod
    def convert_to_string(payload: dict[str, Any]):
        return json.dumps(payload)

    @staticmethod
    def create_message_payload(
            id: Optional[str] = None,
            text: Optional[str] = None,
            ts: Optional[int] = None
    ):
        return {
            "id": id if id is not None else fake.uuid4(),
            "ts": ts if ts is not None else fake.unix_time(),
            "text": text if text is not None else fake.text()
        }
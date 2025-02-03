import json
from typing import Any
from faker import Faker


fake = Faker()


class Payloads:

    @staticmethod
    def convert_to_json(payload: dict[str, Any]) -> str:
        return json.dumps(payload)

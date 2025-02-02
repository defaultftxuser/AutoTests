import allure
import json
from allure_commons.types import AttachmentType


class Helper:

    @staticmethod
    def attach_response(response):
        response = json.dumps(response, indent=4)
        allure.attach(body=response, name="API Response", attachment_type=AttachmentType.JSON)

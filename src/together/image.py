from typing import Any, Dict, Optional

import requests

import together
from together.utils.utils import exit_1, get_logger, verify_api_key


logger = get_logger(str(__name__), log_level=together.log_level)


class Image:
    def __init__(
        self,
    ) -> None:
        verify_api_key(logger)

    @classmethod
    def create(
        self,
        prompt: str,
        model: Optional[str] = "",
        steps: Optional[int] = 50,
        seed: Optional[int] = 42,
        results: Optional[int] = 1,
        height: Optional[int] = 256,
        width: Optional[int] = 256,
    ) -> Dict[str, Any]:
        if model == "":
            model = together.default_image_model

        parameter_payload = {
            "model": model,
            "prompt": prompt,
            "n": results,
            "mode": "text2img",
            "steps": steps,
            "seed": seed,
            "height": height,
            "width": width,
        }

        # HTTP headers for authorization
        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "Content-Type": "application/json",
        }

        # send request
        try:
            response = requests.post(
                together.api_base_complete,
                headers=headers,
                json=parameter_payload,
            )
        except requests.exceptions.RequestException as e:
            logger.critical(f"Response error raised: {e}")
            exit_1(logger)

        try:
            response_json = dict(response.json())
        except Exception as e:
            logger.critical(
                f"JSON Error raised: {e}\nResponse status code = {response.status_code}"
            )
            exit_1(logger)
        return response_json

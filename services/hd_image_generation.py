from typing import Dict, Any, Optional
import requests


def generate_hd_image(
    prompt: str,
    api_key: str,
    model_version: str = "2.2",   # kept only for compatibility
    num_results: int = 1,
    aspect_ratio: str = "1:1",
    sync: bool = True,
    seed: Optional[int] = None,
    negative_prompt: str = "",
    steps_num: Optional[int] = None,
    text_guidance_scale: Optional[float] = None,
    medium: Optional[str] = None,
    prompt_enhancement: bool = False,
    enhance_image: bool = False,
    content_moderation: bool = False,
    ip_signal: bool = False
) -> Dict[str, Any]:

    if not prompt:
        raise ValueError("Prompt is required for image generation")

    if not api_key:
        raise ValueError("Bria API key is required")

    # Current Bria API endpoint
    url = "https://engine.prod.bria-api.com/v2/image/generate"

    headers = {
        "api_token": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Current Bria request body
    data = {
        "prompt": prompt,
        "resolution": "4MP" if enhance_image else "1MP",
        "aspect_ratio": aspect_ratio,
        "sync": sync,
        "output_type": "png",
        "ip_signal": ip_signal,
        "prompt_content_moderation": True,
        "visual_input_content_moderation": True,
        "visual_output_content_moderation": True
    }

    if seed is not None:
        data["seed"] = seed

    # Negative prompt, medium, steps_num, text_guidance_scale,
    # prompt_enhancement and num_results are not sent because
    # they are not part of the current /v2/image/generate schema.

    try:
        print(f"Making request to: {url}")

        # NEVER print the API key
        print("Request parameters:")
        print(data)

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=180
        )

        print(f"Response status: {response.status_code}")

        if not response.ok:
            # Show Bria's actual error instead of hiding it behind
            # "500 Internal Server Error"
            try:
                error_body = response.json()
            except Exception:
                error_body = response.text

            raise RuntimeError(
                f"Bria API returned HTTP {response.status_code}: "
                f"{error_body}"
            )

        result = response.json()

        print("Bria response received successfully.")

        return result

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "Bria API request timed out. "
            "Try again or use async mode."
        )

    except requests.exceptions.RequestException as e:
        raise RuntimeError(
            f"Bria API request failed: {e}"
        )

    except ValueError:
        raise

    except Exception as e:
        raise RuntimeError(
            f"HD image generation failed: {e}"
        )
import json

import requests

from default.common import http

url = "https://stablediffusionapi.com/api/v3/text2img"

payload = json.dumps({
    "key": "S0h4uqwZncHLFvsvL3YbQqFxjFIenEvWInz3y5DJ6QwYm9TQLgs3wtcBsRMt",
    "prompt": "ultra realistic close up portrait ((beautiful pale cyberpunk female with heavy black eyeliner))",
    "negative_prompt": None,
    "width": "512",
    "height": "512",
    "samples": "1",
    "num_inference_steps": "20",
    "seed": None,
    "guidance_scale": 7.5,
    "safety_checker": "yes",
    "multi_lingual": "no",
    "panorama": "no",
    "self_attention": "no",
    "upscale": "no",
    "embeddings_model": None,
    "webhook": None,
    "track_id": None
})

headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)


def text_to_image(url, method, payload):
    return http.request(url, method)

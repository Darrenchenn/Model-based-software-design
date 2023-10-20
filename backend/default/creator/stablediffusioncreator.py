import json

from default.common import http


class StableDiffusion:
    def __init__(self, key, prompt, width, height):
        self.method = "POST"
        self.url = "https://api.stable-diffusion.com/api/v1/generate"
        self.key = key
        self.prompt = prompt
        if width != "":
            self.width = width
        else:
            self.width = "512"
        if height != "":
            self.height = height
        else:
            self.height = "512"

        self.height = height
        self.payload = json.dumps({
            "key": self.key,
            "prompt": self.prompt,
            "negative_prompt": None,
            "width": self.width,
            "height": self.height,
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

    def text_to_pic(self):
        return http.request(self.url, self.method, self.payload)

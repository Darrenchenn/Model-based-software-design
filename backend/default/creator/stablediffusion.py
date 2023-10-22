import json
import logging

from default.common import http, error

logger = logging.getLogger('django')


class StableDiffusion:
    def __init__(self, key, prompt, width, height):
        self.payload = None
        self.method = "POST"
        self.url = ""
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

    def pic_to_pic(self, init_image):
        if self.key == "":
            return error.Error("Please enter your API key").new()
        if init_image == "":
            return error.Error("Please enter an init image").new()
        self.url = "https://stablediffusionapi.com/api/v3/img2img"
        self.payload = json.dumps({
            "key": self.key,
            "prompt": self.prompt,
            "negative_prompt": None,
            "init_image": init_image,
            "width": self.width,
            "height": self.height,
            "samples": "1",
            "num_inference_steps": "30",
            "safety_checker": "no",
            "enhance_prompt": "yes",
            "guidance_scale": 7.5,
            "strength": 0.7,
            "seed": None,
            "webhook": None,
            "track_id": None
        })
        logger.info(self.payload)
        return http.request(self.url, self.method, self.payload)

    def text_to_pic(self):
        if self.key == "":
            return error.Error("Please enter your API key").new()
        self.url = "https://stablediffusionapi.com/api/v3/text2img"
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
        logger.info(self.payload)
        return http.request(self.url, self.method, self.payload)

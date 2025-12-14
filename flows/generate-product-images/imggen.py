import os
import io
from metaflow import profile


class ImgGen:

    def load_model(self, only_load=False):

        from diffusers import DiffusionPipeline
        import torch

        model_name = "Qwen/Qwen-Image"

        if torch.cuda.is_available():
            print("USING CUDA")
            torch_dtype = torch.bfloat16
            device = "cuda"
        else:
            print("NOT USING CUDA")
            torch_dtype = torch.float32
            device = "cpu"

        with profile("loading model"):
            self.pipe = DiffusionPipeline.from_pretrained(
                model_name, torch_dtype=torch_dtype, cache_dir="/model"
            )
            if not only_load:
                self.pipe = self.pipe.to(device)

        model_size = dir_size_gb('/model')
        print(f'Total model size: **{model_size}GB**')

    def prompt(self, prompts_batch, style="Ultra HD, 4K, cinematic composition."):
        import torch

        PROMPT = "Product image without any text - style: {style}. Description: {desc}"
        NEGATIVE = "text, labesl, description"
        prompts = [PROMPT.format(style=style, desc=p) for p in prompts_batch]

        images = self.pipe(
            prompt=prompts,
            negative_prompt=NEGATIVE,
            width=640,
            height=320,
            num_inference_steps=20,
            true_cfg_scale=4.0,
            generator=torch.Generator(device="cuda").manual_seed(42),
        ).images

        for prompt, image in zip(prompts_batch, images):
            buf = io.BytesIO()
            image.save(buf, format="JPEG")
            yield prompt, buf.getvalue()

def dir_size_gb(path):
    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            try:
                fp = os.path.join(root, f)
                total += os.path.getsize(fp)
            except FileNotFoundError:
                pass
    return total / 1024**3

if __name__ == "__main__":
    ImgGen().load_model()

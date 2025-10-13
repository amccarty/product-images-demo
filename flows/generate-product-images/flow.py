import time
from metaflow import (
    FlowSpec,
    profile,
    config_expr,
    current,
    step,
    checkpoint,
    Flow,
    namespace,
    Run,
    card,
    gpu_profile,
    Config,
    kubernetes,
    pypi,
    trigger,
    Parameter,
    environment,
    nebius_checkpoints,
)
from obproject import ProjectFlow

IMG_BATCH_SIZE = 8


def partition(lst, n):
    k = len(lst) // n
    return [lst[i * k : (i + 1) * k] for i in range(n)]

@nebius_checkpoints(**config_expr("config.checkpoint"))
@trigger(event="products_updated")
class ProductImageFlow(ProjectFlow):

    config = Config("config", default="imggen_config.json")
    product_run = Parameter("product-run")
    max_images = Parameter("max-images", default=100)
    num_parallel = Parameter("num-parallel", default=4)

    @gpu_profile(interval=1)
    @kubernetes(compute_pool="obp-nebius-h100-1gpu", **config.compute)
    @checkpoint(load_policy=None)
    @pypi(**config.deps)
    @step
    def start(self):
        import model_loader

        namespace(None)
        self.valid_products = Run(self.product_run).data.valid_products
        self.model_checkpoint = model_loader.load()
        self.descriptions = partition(self.valid_products, self.num_parallel)
        self.next(self.generate_images, foreach="descriptions")

    @card(id="images", type="blank")
    @gpu_profile(interval=1)
    @checkpoint(load_policy=None)
    @kubernetes(compute_pool="obp-nebius-h100-1gpu", **config.compute)
    @pypi(**config.deps)
    @step
    def generate_images(self):
        from images_card import ImagesCard
        from imggen import ImgGen

        # Load model from the designated checkpoint
        gen = ImgGen()
        with profile("Getting model ready"):
            current.checkpoint.load(self.model_checkpoint, path="/model")
            gen.load_model()

        images_card = ImagesCard()
        images_card.start(len(self.input))
        stats = []

        # Generate images in batches of IMG_BATCH_SIZE
        for i in range(0, len(self.input), IMG_BATCH_SIZE):
            t = time.time()
            results = list(gen.prompt(self.input[i : i + IMG_BATCH_SIZE]))
            stats.append((time.time() - t) / IMG_BATCH_SIZE)
            images_card.update(results, i, stats)
            if i > self.max_images:
                break

        self.next(self.join)

    @step
    def join(self, inputs):
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    ProductImageFlow()

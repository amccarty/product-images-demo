from metaflow import current
from metaflow.cards import ProgressBar, Markdown, Image


class ImagesCard:

    def __init__(self):
        self.card = current.card["images"]

    def start(self, num_items):
        self.perf = Markdown("### 🖼️ Generation speed: -")
        self.progress = ProgressBar(max=num_items, label="Images generated")
        self.card.append(self.perf)
        self.card.append(self.progress)
        self.card.refresh()

    def update(self, results, i, stats):
        ms = int(1000.0 * sum(stats) / len(stats))
        self.perf.update(f"### 🖼️ Generation speed: **{ms}ms** / image")
        self.progress.update(i + 1)
        for desc, img in results:
            self.card.append(Markdown(desc))
            self.card.append(Image(img))
        self.card.refresh()

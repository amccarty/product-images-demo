import time
import os
from metaflow import (
    FlowSpec,
    Parameter,
    step,
    snowpark,
    current,
    pypi,
    card,
    Config,
    config_expr,
    gpu_profile,
    trigger_on_finish,
    kubernetes,
    environment,
)
from obproject import ProjectFlow
from metaflow.integrations import ArgoEvent
from collections import Counter

from snowpark_card import snowpark_card

@trigger_on_finish(flow='SensorFlow')
class RetrieveDescriptions(ProjectFlow):

    min_length = Parameter("min-length", default=10)
    config = Config("config", default="snowpark_config.json")

    @step
    def start(self):
        self.next(self.mid)

    # @snowpark_card
    # @snowpark(**config.compute)
    @pypi(packages=config.deps)
    @card(id="data", type="blank", refresh_interval=1)
    @step
    def mid(self):
        from data_card import DataCard
        import langid

        SQL = (
            "select SCR:data:description as description "
            "from amazon_product_chunk limit 2500"
        )

        card = DataCard()

        # Run query
        card.start_query(SQL)
        start = time.time()
        rows = current.snowflake.session().sql(SQL).collect(block=True)
        duration = int((time.time() - start) * 1000)
        card.query_done(duration, len(rows))

        stats = Counter()
        print(f"num rows {len(rows)}")
        self.valid_products = []

        # Process rows
        for i, row in enumerate(rows):
            # filter descriptions that are too short
            if len(row.DESCRIPTION.split()) > self.min_length:
                # Detect language of the description
                lang, score = langid.classify(row.DESCRIPTION)
                stats[lang] += 1
                if lang == "en":
                    self.valid_products.append(row.DESCRIPTION)

                print(f"[{lang} {score}] {row.DESCRIPTION}")
            card.update_processing(stats, i)

        card.update_processing(stats)
        self.next(self.end)

    @step
    def end(self):
        run = f"{current.flow_name}/{current.run_id}"
        ArgoEvent("products_updated").publish({"product-run": run})


if __name__ == "__main__":
    RetrieveDescriptions()

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
        self.next(self.query)

    # @snowpark_card
    # @snowpark(**config.compute)
    @pypi(packages=config.deps)
    @card(id="data", type="blank", refresh_interval=1)
    @step
    def query(self):
        from data_card import DataCard
        import langid

        SQL = (
            "SELECT SCR:data:description as description "
            "FROM ECOMMERCE_PRODUCT_DATA_SET.JSON.amazon_product_chunk "
            "LIMIT 2500"
        )

        card = DataCard()

        # Run query
        card.start_query(SQL)
        start = time.time()

        # Use Metaflow Snowflake integration instead of Snowpark
        from metaflow import Snowflake

        with Snowflake(integration=self.config.compute.external_integration[0]) as cn:
            with cn.cursor() as cur:
                cur.execute(SQL)
                rows = cur.fetchall()

        duration = int((time.time() - start) * 1000)
        card.query_done(duration, len(rows))

        stats = Counter()
        print(f"num rows {len(rows)}")
        self.valid_products = []

        # Process rows
        for i, row in enumerate(rows):
            # Extract description from tuple (first column)
            description = row[0] if row[0] is not None else ""

            # filter descriptions that are too short
            if len(description.split()) > self.min_length:
                # Detect language of the description
                lang, score = langid.classify(description)
                stats[lang] += 1
                if lang == "en":
                    self.valid_products.append(description)

                print(f"[{lang} {score}] {description}")
            card.update_processing(stats, i)

        card.update_processing(stats)
        self.next(self.end)

    @step
    def end(self):
        run = f"{current.flow_name}/{current.run_id}"
        ArgoEvent("products_updated").publish({"product-run": run})


if __name__ == "__main__":
    RetrieveDescriptions()

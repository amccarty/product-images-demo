from metaflow import current
from metaflow.cards import Markdown, Table, ProgressBar, VegaChart

import chart


def show(txt):
    current.card["data"].append(Markdown(txt))


def refresh():
    current.card["data"].refresh()


class DataCard:

    def start_query(self, sql):
        show(f"### Executing query\n\n```\n{sql}\n```\n")
        refresh()

    def query_done(self, duration, num_rows):
        show(f"Query executed in **{duration}ms**, **{num_rows}** rows returned")
        show("### Processing rows")
        self.p = ProgressBar(max=num_rows, label="Rows processed")
        current.card["data"].append(self.p)
        self.viz = VegaChart(chart.make_chart([]))
        show("#### Distribution of languages")
        current.card["data"].append(self.viz)
        refresh()

    def update_processing(self, stats, i=None):
        if i is None or not (i % 100):
            self.viz.update(chart.make_chart(stats.items()))
        if i is not None:
            self.p.update(i + 1)
        refresh()

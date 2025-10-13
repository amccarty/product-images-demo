import os
from metaflow import StepMutator, current, user_step_decorator
from metaflow.cards import Markdown, Table


@user_step_decorator
def populate_snowpark_card(step_name, flow, inputs=None, attr=None):
    rows = []
    for k, v in os.environ.items():
        if k.startswith("SNOWFLAKE_"):
            rows.append([k[len("SNOWFLAKE_") :], v])
    current.card["snowpark"].append(Markdown("# ❄️ Snowpark job"))
    current.card["snowpark"].append(Table(rows))
    current.card["snowpark"].refresh()
    yield


class snowpark_card(StepMutator):

    def mutate(self, mutable_step):
        mutable_step.add_decorator(
            "card", deco_kwargs={"id": "snowpark", "type": "blank"}
        )
        mutable_step.add_decorator(populate_snowpark_card)

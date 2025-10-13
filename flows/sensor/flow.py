from datetime import datetime
from itertools import islice
import time

from metaflow import (
    FlowSpec,
    step,
    config_expr,
    project,
    schedule,
    Parameter,
    Config,
    conda,
    card,
    Flow,
    current,
)
from metaflow.cards import Markdown
from metaflow.integrations import ArgoEvent
from obproject import ProjectFlow

from sensorbase import SensorBase


class SkipTrigger(Exception):
    pass


class SensorFlow(SensorBase, ProjectFlow):
    force = Parameter("force-trigger", default=False)

    @card(type="blank")
    @snowflake
    @step
    def start(self):
        if self.force:
            current.card.append(Markdown("*Force is true - ignoring previous value*"))
            prev = None
        else:
            try:
                # The latest run is currently executing run so we have to pick the one
                # before this
                run = list(islice(Flow(current.flow_name), 2))[1]
                ago = (datetime.now() - run.finished_at).seconds // 60
                current.card.append(
                    Markdown(
                        f"Comparing to previous run **`{run.pathspec}`** from {ago} minutes ago"
                    )
                )
                prev = run["start"].task["value"].data
            except:
                current.card.append(Markdown(f"*Previous successful runs not found*"))
                prev = None
        [(self.value,)] = self.query_snowflake(template="sensor", card=True)
        print(f"Previous value {prev}, new value {self.value}")
        if self.value == prev:
            print("no changes")
            self.trigger = False
            current.card.append(
                Markdown(f"## 🔄 No changes\n\nThe value is still `{self.value}`")
            )
        else:
            print("Triggering")
            self.trigger = True
            current.card.append(
                Markdown(
                    f"## 🚀 Value changed to `{self.value}`\n\nThe old value was `{prev}`"
                )
            )
        self.next(self.end)

    @step
    def end(self):
        event_name = self.config.sensor.get("event_name")
        key = self.config.sensor.get("payload_key", "value")
        if event_name:
            print(f"Publishing event {event_name}")
            ArgoEvent(event_name).publish({key: self.value})
        else:
            if self.trigger:
                print("Finishing the run successfully to create an event")
            else:
                raise SkipTrigger(
                    "Not an error - failing this run on purpose "
                    "to avoid triggering flows downstream"
                )


if __name__ == "__main__":
    SensorFlow()

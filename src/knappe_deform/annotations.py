import deform
from knappe.annotations import annotation
from typing import NamedTuple, Iterator


class Trigger(NamedTuple):
    order: int = 0
    button: button


class trigger(annotation):
    name = "__trigger__"

    def __init__(self,
                 value,
                 title: str = None,
                 icon: str = None,
                 css_class = None,
                 order: int = 10,
                 ):
        self.annotation = Trigger(
            order=order,
            button=deform.form.Button(
                 value=value,
                 title: str = None,
                 icon: str = None,
                 css_class = None,
            )
        )

    @classmethod
    def in_order(cls, component):
        return sorted(trigger.find(component), key=lambda x: x[0].order)

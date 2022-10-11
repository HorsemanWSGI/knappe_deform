import pathlib
import colander
import typing as t
from chameleon.zpt.template import PageTemplateFile
from knappe.meta import HTTPMethodEndpointMeta
from .annotations import trigger, Trigger


form_template = PageTemplateFile(
    str(pathlib.Path(__file__).parent / "form.pt")
)


class FormPage(metaclass=HTTPMethodEndpointMeta):

    schema: t.Type[colander.Schema]

    def __init__(self):
        triggers = trigger.in_order(self)
        self.actions = {('trigger', t.value): m for t, m in triggers}
        self.buttons = tuple((t.button for t, m in triggers))

    def get_form(self, request):
        schema = self.schema().bind(request=request)
        return deform.form.Form(schema, buttons=self.buttons)

    @html('form', default_template=form_template)
    def GET(self, request):
        form = self.get_form(request)
        return {
            "error": None,
            "rendered_form": form.render()
        }

    @html('form', default_template=form_template)
    def POST(self, request):
        found = tuple(set(self.actions) & set(request.data.form))
        if len(found) != 1:
            raise HTTPError(
                400, body='Could not resolve an action for the form.')
        action = self.actions[found[0]]
        return action(request)

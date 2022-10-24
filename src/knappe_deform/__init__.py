import pathlib
import typing as t
import deform
import colander
from chameleon.zpt.template import PageTemplateFile
from knappe.decorators import html
from knappe import HTTPError
from knappe.meta import HTTPMethodEndpointMeta
from .annotations import trigger, Trigger


form_template = PageTemplateFile(
    str(pathlib.Path(__file__).parent / "form.pt")
)


class FormPage(metaclass=HTTPMethodEndpointMeta):

    def __init__(self):
        triggers = trigger.in_order(self)
        self.actions = {t.form_id: m for t, m in triggers}
        self.buttons = tuple((t.button for t, m in triggers))

    def get_schema(self, request) -> t.Type[colander.Schema]:
        raise NotImplementedError('Implement your own.')

    def get_form(self, request, data=None) -> deform.form.Form:
        """Returns a form
        """
        schema = self.get_schema(request)
        bound = schema.bind(request=request, data=data)
        return deform.form.Form(bound, buttons=self.buttons)

    def get_initial_data(self, request) -> dict:
        return {}

    @html('form', default_template=form_template)
    def GET(self, request) -> dict:
        data = self.get_initial_data(request)
        form = self.get_form(request, data)
        return {
            "error": None,
            "rendered_form": form.render(data)
        }

    @html('form', default_template=form_template)
    def POST(self, request):
        found = tuple(set(self.actions) & set(request.data.form))
        if len(found) != 1:
            raise HTTPError(
                400, body='Could not resolve an action for the form.')
        action = self.actions[found[0]]
        return action(request)

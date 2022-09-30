from django.forms.widgets import Widget

"""_summary_
One last touch we will apply to our basket is a better widget to manage
changes to product quantities. We want to present separate bigger buttons
with plus and minus signs to make it easy for the user to change the numbers
In order to do so, we need to change the way the quantity field is
rendered in forms. Because the field is inheriting from IntegerField,
Django by default will use the built-in NumberInput widget.
The widget is referring to an external template for its HTML. Here we
also define a Media subclass with some extra CSS and JavaScript to include
in the output. While template_name is a specific widget functionality,
defining a Media subclass is a functionality that can be applied to both widgets and forms as well.
We will use this HTML for the widget (main/templates/widgets/plusminusnumber.html):
"""


class PlusMinusNumberInput(Widget):
    template_name = 'main/widgets/plusminusnumber.html'

    class Media:
        css = {
            'all': ('css/plusminusnumber.css',)
        }
        js = ('js/plusminusnumber.js',)

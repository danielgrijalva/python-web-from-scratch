from cgi import parse_qs, FieldStorage
from app.template import Templite
from .abstract_view import AbstractView

class Dashboard(AbstractView):
    renderer = Templite('dashboard')

    def serve(self):
        products = self.model.select_all()
        if products:
            html = self.renderer.render({'products': products, 'alerts': None})
            status, response_headers = self.get_response_data(html)
            self.start_response(status, response_headers)

            return [html.encode('utf-8')]
        else:
            return self.redirect('/add/')
            
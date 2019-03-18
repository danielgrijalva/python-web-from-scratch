from cgi import parse_qs, FieldStorage
from app.template import Templite
from .abstract_view import AbstractView

class GetProduct(AbstractView):
    renderer = Templite('product')

    def serve(self):
        product_id = parse_qs(self.environ['QUERY_STRING'])['id'][0]
        product = self.model.select_one(product_id)
        html = self.renderer.render({'product': product})

        status, response_headers = self.get_response_data(html)
        self.start_response(status, response_headers)    

        return [html.encode('utf-8')]   

from cgi import parse_qs, FieldStorage
from app.template import Templite
from .abstract_view import AbstractView

class AddProduct(AbstractView):
    renderer = Templite('add_product')

    def serve(self, alerts=None):
        if self.environ['REQUEST_METHOD'] == 'POST':
            form = FieldStorage(
                    fp=self.environ['wsgi.input'], 
                    environ=self.environ,
                )
                
            data = {
                'name': form['name'].value,
                'description': form['description'].value,
                'price': form['price'].value,
                'stock': form['stock'].value,
            }

            try:
                inserted_id = self.model.insert(data)
                alerts = [{
                        'context': 'success', 
                        'message': '<a href="/product?id={id}">Product #{id}</a> added.'.format(id=inserted_id)
                    }]
            except Exception as e:
                print(e)
            
        html = self.renderer.render({'alerts': alerts})
        status, response_headers = self.get_response_data(html)
        self.start_response(status, response_headers)

        return [html.encode('utf-8')]

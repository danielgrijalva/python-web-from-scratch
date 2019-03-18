from cgi import parse_qs, FieldStorage
from app.template import Templite
from .abstract_view import AbstractView

class EditProduct(AbstractView):
    renderer = Templite('edit_product')

    def serve(self):
        product_id = parse_qs(self.environ['QUERY_STRING'])['id'][0]
        product = self.model.select_one(product_id)

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
                self.model.update(data, product_id)
                # alerts = [{
                #     'context': 'success',
                #     'message': 'Product added.'
                # }]
            except Exception as e:
                print(e)

            return self.redirect('/product?id={}'.format(product_id))
            
        html = self.renderer.render({'product': product, 'alerts': None})
        status, response_headers = self.get_response_data(html)
        self.start_response(status, response_headers)

        return [html.encode('utf-8')]

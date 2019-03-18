from cgi import parse_qs, FieldStorage
from app.template import Templite
from .abstract_view import AbstractView

class DeleteProduct(AbstractView):
    renderer = Templite('product')

    def serve(self):
        if self.environ['REQUEST_METHOD'] == 'POST':
            form = FieldStorage(
                    fp=self.environ['wsgi.input'], 
                    environ=self.environ,
                )
            
            product_id = form['product_id'].value
            product_name = self.model.select_one(product_id)['name']

            self.model.delete(product_id)

            # alerts = [{
            #             'context': 'danger', 
            #             'message': 'Deleted {}'.format(product_name)
            #         }]

            return self.redirect('/')
            
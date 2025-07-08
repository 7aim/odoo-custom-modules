from odoo import models, fields

class LibraryBookCategory(models.Model):
    _name = 'library.book.category'
    _description = 'Library Book Category'

    name = fields.Char(string='Name', required=True)

    category_book_ids = fields.One2many(
        'library.book',      # Əlaqəli model (hansı modelin obyektlərini göstərəcək)
        'category_ids',         # Əlaqəli modeldəki geriyə-əlaqə sahəsi (bizim Many2one sahəmiz)
        string='Books'       # Sahənin interfeysdəki adı
    )
# -*- coding: utf-8 -*-
from odoo import models, fields

class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Library Author'

    name = fields.Char(string='Name', required=True)
    birth_date = fields.Date(string='Date of Birth')

    book_ids = fields.One2many(
        'library.book',      # Əlaqəli model (hansı modelin obyektlərini göstərəcək)
        'author_id',         # Əlaqəli modeldəki geriyə-əlaqə sahəsi (bizim Many2one sahəmiz)
        string='Books'       # Sahənin interfeysdəki adı
    )
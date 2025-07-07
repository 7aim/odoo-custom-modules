from odoo import models, fields

class AssignCategoryWizard(models.TransientModel):
    _name = 'library.assign.category.wizard'
    _description = 'Assign Category Wizard'

    category_id = fields.Many2one('library.book.category', string='Category', required=True)

    def action_assign_category(self):
        # Seçilmiş kitabların ID-lərini kontekstdən götürürük
        book_ids = self.env.context.get('active_ids', [])
        if book_ids:
            # Həmin ID-lərə uyğun kitab qeydlərini tapırıq
            books = self.env['library.book'].browse(book_ids)
            # Seçilmiş kateqoriyanı bütün seçilmiş kitablara əlavə edirik
            books.write({'category_ids': [(4, self.category_id.id)]})

        # Pəncərəni bağlayırıq
        return {'type': 'ir.actions.act_window_close'}
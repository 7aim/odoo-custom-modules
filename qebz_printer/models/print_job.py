from odoo import api, models

class PrintJob(models.Model):
    _inherit = 'pos.print.job' # Və ya yeni model

    @api.model
    def get_receipt_content(self, order_id):
        order = self.env['pos.order'].browse(order_id)
        if not order:
            return ""

        # QWeb şablonunu render et
        rendered_receipt = self.env['ir.qweb']._render(
            'pos_qz_printer.qz_pos_receipt_template', 
            {'order': order}
        )
        return rendered_receipt
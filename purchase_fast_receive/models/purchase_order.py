from odoo import models, fields, api
import time

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_fast_receive(self):
        """Tek tıkla satın alma işlemini tamamla"""
        # Önce siparişi onayla
        if self.state in ['draft', 'sent', 'to approve']:
            self.button_confirm()
        
        # Siparişin onaylanmasını bekle
        self.env.cr.commit()
        self.invalidate_recordset()
        
        # Biraz bekle ki picking'ler oluşsun
        time.sleep(1)
        
        # Origin'a göre picking'leri bul
        pickings = self.env['stock.picking'].search([
            ('origin', '=', self.name),
            ('picking_type_code', '=', 'incoming')  # Sadece gelen transferler
        ])
        
        success_count = 0
        
        for picking in pickings:
            try:
                # Picking state'ini kontrol et
                if picking.state == 'draft':
                    picking.action_confirm()
                
                if picking.state in ['confirmed', 'waiting']:
                    picking.action_assign()
                
                # Picking'i yeniden yükle
                picking.invalidate_recordset()
                picking = picking.browse(picking.id)
                
                if picking.state in ['assigned', 'partially_available']:
                    # Move line'ları kontrol et ve oluştur
                    if not picking.move_line_ids:
                        for move in picking.move_ids:
                            if move.state in ['assigned', 'partially_available']:
                                # Move line oluştur
                                self.env['stock.move.line'].create({
                                    'move_id': move.id,
                                    'picking_id': picking.id,
                                    'product_id': move.product_id.id,
                                    'location_id': move.location_id.id,
                                    'location_dest_id': move.location_dest_id.id,
                                    'quantity': move.product_uom_qty,
                                    'product_uom_id': move.product_uom.id,
                                })
                    
                    # Move'ları done yap
                    for move in picking.move_ids:
                        if move.state in ['assigned', 'partially_available']:
                            move.quantity_done = move.product_uom_qty
                    
                    # Move line'ları done yap
                    for move_line in picking.move_line_ids:
                        if move_line.quantity == 0:
                            move_line.quantity = move_line.reserved_quantity or move_line.product_uom_qty
                    
                    # Picking'i validate et
                    res = picking.button_validate()
                    
                    # Wizard handling
                    if isinstance(res, dict):
                        if res.get('res_model') == 'stock.immediate.transfer':
                            wizard = self.env[res['res_model']].browse(res['res_id'])
                            wizard.process()
                        elif res.get('res_model') == 'stock.backorder.confirmation':
                            wizard = self.env[res['res_model']].browse(res['res_id'])
                            wizard.process_cancel_backorder()  # Backorder'ı iptal et, hepsini al
                    
                    success_count += 1
                    
            except Exception as e:
                continue
        
        self.env.cr.commit()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Başarılı!' if success_count > 0 else 'Hata!',
                'message': f'{success_count} adet transfer tamamlandı. Ürünler depoya alındı.' if success_count > 0 else 'Transfer işlemi başarısız!',
                'type': 'success' if success_count > 0 else 'danger',
                'sticky': False,
            }
        }
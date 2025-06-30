# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import re

class PicnicEntry(models.Model):
    _name = 'picnic.entry'
    _description = 'Piknik Giriş Qeydiyyatı'

    name = fields.Char(string="Qeydiyyat Nömrəsi", required=True, copy=False, readonly=True, default=lambda self: 'Yeni')
    masin_nomresi = fields.Char(string="Maşın Nömrəsi", required=True)
    telefon_nomresi = fields.Char(string="Telefon Nömrəsi", required=True)
    adam_sayi = fields.Integer(string="Adam Sayı", default=1, required=True)
    #adlar = fields.Text(string="Qonaqların adları")
    guest_ids = fields.One2many('picnic.guest', 'entry_id', string="Qonaqlarin adlari")
    
    
    giris_vaxti = fields.Datetime(string="Giriş Vaxtı", default=fields.Datetime.now, required=True)
    cixis_vaxti = fields.Datetime(string="Çıxış Vaxtı")
    
    zona = fields.Many2one('picnic.zone', string="Zona", required=True, ondelete='restrict')

    # Şirket
    company_id = fields.Many2one('res.company', string='Şirkət', default=lambda self: self.env.company)
    # Valyuta
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string='Valyuta')
    
    nefer_basi_odenis = fields.Monetary(string="Bir Nəfər Üçün Məbləğ", default = 5.0, currency_field='currency_id')
    
    umumi_odenis = fields.Monetary(
        string="Ümumi Məbləğ", 
        compute='_compute_umumi_odenis', 
        store=True,
        currency_field='currency_id'
    )

    qebul_eden_sexs = fields.Many2one('accepting.person', string="Qebul eden şexs", required=True, ondelete='restrict')
    
    state = fields.Selection([
        ('daxil_oldu', 'Daxil Oldu'),
        ('cixis_etdi', 'Çıxış Etdi'),
        ('cancel', 'Ləğv Edildi')  
    ], string='Status', default='daxil_oldu', required=True)


    # Umumi odenisin hesablanmasi
    @api.depends('nefer_basi_odenis', 'adam_sayi') # bu ikisinden biri deyisse avtomatik funksiyani ise sal
    def _compute_umumi_odenis(self): # compute ile baslamasi bunun hesablama funksiyasi oldugunu gosterir
        for record in self: # her bir qeydi ayri ayriliqda emal edir
            record.umumi_odenis = record.nefer_basi_odenis * record.adam_sayi
    
    @api.onchange('adam_sayi')
    def _onchange_adam_sayi(self):
        # Mənfi dəyərlərin qarşısını al
        if self.adam_sayi < 0:
            self.adam_sayi = 0

        current_lines = self.guest_ids
        target_count = self.adam_sayi
        current_count = len(current_lines)

        if target_count > current_count:
            # Say artırılıbsa: Yeni virtual qeydlər (recordset) yarat və mövcud olanla birləşdir
            new_records = self.env['picnic.guest']  # Boş bir recordset yaradırıq
            for _ in range(target_count - current_count):
                # new() metodu ilə yaddaşda virtual bir qeyd yaradıb |= operatoru ilə recordset-ə əlavə edirik
                new_records |= self.env['picnic.guest'].new({'name': ''})
            
            self.guest_ids |= new_records

        elif target_count < current_count:
            self.guest_ids = current_lines[:target_count]
            
    # Umumi yoxlanis
    def _perform_all_validations(self, vals): # vals butun deyerleri ozunde dict kimi tutur
        if 'masin_nomresi' in vals and vals['masin_nomresi']:
            pattern = re.compile(r'^\d{2}[A-Z]{2}\d{3}$')
            if not pattern.match(vals['masin_nomresi'].upper()):
                raise ValidationError("Maşın nömrəsi düzgün formatda deyil! Gözlənilən format: 99AA999")

        if 'telefon_nomresi' in vals and vals['telefon_nomresi']:
            pattern1 = re.compile(r'^\+994\d{9}$')
            pattern2 = re.compile(r'^\d{10}$')
            if not pattern1.match(vals['telefon_nomresi']) and not pattern2.match(vals['telefon_nomresi']):
                raise ValidationError("Telefon nömrəsi düzgün formatda deyil! Gözlənilən format: +994556667788 ya da 5556667788")

        if 'adam_sayi' in vals and vals['adam_sayi'] <= 0:
            raise ValidationError("Adam sayı müsbət ədəd olmalıdır!")
        
        if 'nefer_basi_odenis' in vals and vals['nefer_basi_odenis'] < 0: 
            raise ValidationError("Bir nəfər üçün ödəniş məbləği mənfi ola bilməz!")
        
    def action_cixis_etdi(self):
        self.cixis_vaxti = fields.Datetime.now()
        self.state = 'cixis_etdi'

    def action_cancel(self):
        for record in self:
            # Yoxlayırıq ki, artıq çıxış etmiş bir qeydi ləğv etməyə çalışmasınlar
            if record.state == 'cixis_etdi':
                # Bu, istəyə bağlıdır, amma yaxşı praktikadır
                raise UserError("Artıq çıxış etmiş bir qeydi ləğv etmək olmaz!")
            
            # Qeydin statusunu 'cancel' olaraq dəyişirik
            record.state = 'cancel'
        return True
    
    @api.model
    def create(self, vals):
        # Yeni qeyd yaradılarkən yoxlamaları işə sal
        self._perform_all_validations(vals)

        # Ardıcıllıq nömrəsi məntiqi
        if vals.get('name', 'Yeni') == 'Yeni':
            vals['name'] = self.env['ir.sequence'].next_by_code('picnic.entry') or 'Yeni'
        
        # Odoo-nun standart create funksiyasını çağır
        return super(PicnicEntry, self).create(vals)

    def write(self, vals):
        # Əvvəlcə bütün yoxlamaları çağırırıq
        self._perform_all_validations(vals)
        
        # Odoo-nun standart write funksiyasını çağır
        return super(PicnicEntry, self).write(vals)
    

    # piknik_qeydiyyat/models/picnic_entry.py
    def action_print_receipt(self):
        self.ensure_one()
        # Qəbz üçün mətn formatında data hazırla
        receipt_text = f"""
        {self.company_id.name.center(32)}
        --------------------------------
        QEBZ: {self.name}
        --------------------------------
        Masin Nomresi: {self.masin_nomresi}
        Giris Vaxti: {fields.Datetime.context_timestamp(self, self.giris_vaxti).strftime('%d/%m/%y %H:%M')}
        Adam Sayi: {self.adam_sayi}
        Umumi Mebleg: {self.umumi_odenis} AZN
        --------------------------------
        Qebul etdi: {self.qebul_eden_sexs.name}
        """

        # Yeni çap tapşırığı yarat (direct.print.job modelinə)
        self.env['direct.print.job'].create({
            'data_to_print': receipt_text,
            'printer_name': 'Xprinter XP-Q80C'
        })

        # İstifadəçiyə bildiriş göstər
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Uğurlu',
                'message': 'Çap tapşırığı növbəyə qoyuldu.',
                'sticky': False,
            }
        }
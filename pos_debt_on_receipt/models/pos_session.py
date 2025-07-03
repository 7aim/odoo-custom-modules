# -*- coding: utf-8 -*-
from odoo import models

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_res_partner(self):
        # Standart parametrləri alırıq
        params = super()._loader_params_res_partner()
        # Sahələr siyahısına öz yeni sahəmizi əlavə edirik
        params['search_params']['fields'].append('customer_old_due')
        return params
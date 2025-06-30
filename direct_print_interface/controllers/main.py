# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, route
import json

class DirectPrintController(http.Controller):

    @route('/direct_print/get_job', type='json', auth='user', methods=['POST'])
    def get_print_job(self, printer_name, **kwargs):
        job = request.env['direct.print.job'].search([
            ('state', '=', 'pending'),
            ('printer_name', '=', printer_name)
        ], limit=1)

        if not job:
            return {'status': 'no_job'}

        # Tapşırığı tapdıqda dərhal statusunu dəyişib yadda saxlamaq önəmlidir
        # ki, eyni tapşırıq ikinci dəfə göndərilməsin
        job.write({'state': 'printed'})
        request.env.cr.commit()

        return {
            'status': 'success',
            'job_id': job.id,
            'data': job.data_to_print,
        }
# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class PrintJobController(http.Controller):
    """
    Browser-də çap etmək üçün controller
    """
    
    @http.route('/print/job/<int:job_id>', type='http', auth='user')
    def print_job_preview(self, job_id):
        """
        Print job-u browser-də göstər və çap et
        """
        # Bazadan job-u al
        job = request.env['pos.print.job'].browse(job_id)
        if not job.exists():
            return request.not_found()
        
        # HTML səhifəni hazırla
        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{job.name}</title>
            <style>
                body {{ 
                    font-family: 'Courier New', monospace; 
                    font-size: 12px; 
                    margin: 20px;
                }}
                .receipt {{ 
                    max-width: 300px; 
                    margin: 0 auto; 
                    padding: 20px;
                    border: 1px solid #ddd;
                }}
                .no-print {{ 
                    text-align: center;
                    margin: 20px 0;
                }}
                .print-btn {{
                    background: #007bff;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    margin: 0 10px;
                    cursor: pointer;
                }}
                /* Çap edərkən düymələri gizlə */
                @media print {{
                    .no-print {{ display: none; }}
                    .receipt {{ border: none; }}
                }}
            </style>
        </head>
        <body>
            <!-- Çap düymələri -->
            <div class="no-print">
                <button class="print-btn" onclick="window.print()">
                    🖨️ Çap Et
                </button>
                <button class="print-btn" onclick="window.close()">
                    ❌ Bağla
                </button>
            </div>
            
            <!-- Receipt məzmunu -->
            <div class="receipt">
                <pre>{job.content}</pre>
            </div>
            
            <script>
                // Çap edildikdən sonra status yenilə
                window.addEventListener('afterprint', function() {{
                    fetch('/print/job/{job_id}/mark_printed', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }}
                    }});
                }});
            </script>
        </body>
        </html>
        '''
        
        return html_content
    
    @http.route('/print/job/<int:job_id>/mark_printed', type='json', auth='user')
    def mark_job_printed(self, job_id):
        """
        Print job-u çap edilmiş kimi işarələ
        """
        job = request.env['pos.print.job'].browse(job_id)
        if job.exists():
            job.write({'status': 'printed'})
            return {'success': True}
        return {'success': False}

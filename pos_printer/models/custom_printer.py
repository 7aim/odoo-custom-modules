from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

try:
    import requests
except ImportError:
    _logger.warning("requests library not found. Install with: pip install requests")
    requests = None

class CustomPrinter(models.Model):
    _name = 'custom.printer'
    _description = 'Custom Printer Management'

    name = fields.Char('Printer Name', required=True)
    api_url = fields.Char('API URL', default='http://127.0.0.1:8765')
    is_active = fields.Boolean('Active', default=True)
    printer_type = fields.Selection([
        ('receipt', 'Receipt Printer'),
        ('label', 'Label Printer'),
        ('document', 'Document Printer')
    ], default='receipt')
    test_content = fields.Text('Test Content', default="""MAĞAZA ADI
123 Küçə, Şəhər
Tel: 012-345-67-89
--------------------------------
Tarix: 17.07.2025 15:30
Qəbz №: 001
--------------------------------
Çörək                    2x1.50
                        = 3.00
Süd                      1x2.00
                        = 2.00
--------------------------------
CƏMİ:               5.00 AZN

Təşəkkür edirik!
Yenidən gələcəyinizi gözləyirik""")

    def send_print_job(self, print_data, print_type="receipt"):
        """Çap işini göndərir - təkmilləşdirilmiş"""
        if not requests:
            return {'success': False, 'error': 'requests library not available'}
            
        try:
            payload = {
                'printer': self.name,
                'data': print_data,
                'type': print_type
            }
            
            response = requests.post(
                f"{self.api_url}/print",
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                return {'success': True, 'message': 'Print successful'}
            else:
                return {'success': False, 'error': f'Print failed: {response.text}'}
                
        except Exception as e:
            _logger.error(f"Print job error: {e}")
            return {'success': False, 'error': str(e)}

    def send_formatted_receipt(self, receipt_data):
        """Formatlanmış qəbz göndərir"""
        if not requests:
            return {'success': False, 'error': 'requests library not available'}
            
        try:
            payload = {
                'printer': self.name,
                'receipt': receipt_data
            }
            
            response = requests.post(
                f"{self.api_url}/print/formatted",
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                return {'success': True, 'message': 'Formatted receipt printed'}
            else:
                return {'success': False, 'error': f'Print failed: {response.text}'}
                
        except Exception as e:
            _logger.error(f"Formatted print error: {e}")
            return {'success': False, 'error': str(e)}

    def test_connection(self):
        """API bağlantısını test edir"""
        if not requests:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error!',
                    'message': 'requests library not available',
                    'type': 'danger'
                }
            }
            
        try:
            response = requests.get(f"{self.api_url}/status", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Success!',
                        'message': f'API connected successfully! Status: {data.get("status", "unknown")}',
                        'type': 'success'
                    }
                }
            else:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Error!',
                        'message': f'API connection failed: {response.status_code}',
                        'type': 'danger'
                    }
                }
                
        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error!',
                    'message': f'Connection failed: {str(e)}',
                    'type': 'danger'
                }
            }

    def sync_printers(self):
        """API-dən printerləri sinxronlaşdırır"""
        if not requests:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error!',
                    'message': 'requests library not available',
                    'type': 'danger'
                }
            }
            
        try:
            response = requests.get(f"{self.api_url}/printers", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                printers = data.get('printers', [])
                
                # Yeni printerləri yarat
                created_count = 0
                for printer_info in printers:
                    printer_name = printer_info.get('name')
                    if printer_name:
                        existing = self.search([('name', '=', printer_name)], limit=1)
                        if not existing:
                            self.create({
                                'name': printer_name,
                                'api_url': self.api_url,
                                'printer_type': 'receipt',
                                'is_active': True
                            })
                            created_count += 1
                
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Success!',
                        'message': f'Found {len(printers)} printers, created {created_count} new records',
                        'type': 'success'
                    }
                }
            else:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Error!',
                        'message': f'Failed to get printers: {response.status_code}',
                        'type': 'danger'
                    }
                }
                
        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error!',
                    'message': f'Sync failed: {str(e)}',
                    'type': 'danger'
                }
            }

    def test_print(self):
        """Test çapı edir - yaxşılaşdırılmış"""
        result = self.send_print_job(self.test_content, "receipt")
        
        if result['success']:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Success!',
                    'message': 'Test print successful - formatlanmış',
                    'type': 'success'
                }
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error!',
                    'message': f'Print failed: {result["error"]}',
                    'type': 'danger'
                }
            }
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

try:
    import requests
except ImportError:
    _logger.warning("requests library not found. Install with: pip install requests")
    requests = None

try:
    import json
except ImportError:
    json = None

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
    test_content = fields.Text('Test Content', default="Test Print\n-----------\nHello World!\nBu test çapıdır.")

    @api.model
    def get_available_printers(self):
        """API-dən mövcud printerləri alır"""
        if not requests:
            _logger.error("requests library not available")
            return []
            
        try:
            response = requests.get(f"{self.api_url}/printers", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('printers', [])
        except Exception as e:
            _logger.error(f"Printer API error: {e}")
            return []

    def send_print_job(self, print_data):
        """Çap işini göndərir"""
        if not requests:
            return {'success': False, 'error': 'requests library not available'}
            
        try:
            payload = {
                'printer': self.name,
                'data': print_data
            }
            
            response = requests.post(
                f"{self.api_url}/print",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                return {'success': True, 'message': 'Print successful'}
            else:
                return {'success': False, 'error': 'Print failed'}
                
        except Exception as e:
            _logger.error(f"Print job error: {e}")
            return {'success': False, 'error': str(e)}

    def test_connection(self):
        """API connection test edir"""
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
            response = requests.get(f"{self.api_url}/status", timeout=5)
            if response.status_code == 200:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Success!',
                        'message': 'API connection successful',
                        'type': 'success'
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
        """API-dən printerləri sync edir"""
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
            printers = self.get_available_printers()
            for printer_data in printers:
                existing = self.search([('name', '=', printer_data['name'])])
                if not existing:
                    self.create({
                        'name': printer_data['name'],
                        'printer_type': 'receipt',
                        'is_active': True
                    })
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Success!',
                    'message': f'{len(printers)} printers synced',
                    'type': 'success'
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
        """Test çapı edir"""
        result = self.send_print_job(self.test_content)
        
        if result['success']:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Success!',
                    'message': 'Test print successful',
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
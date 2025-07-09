/** @odoo-module */

// Lazım olan modulları import edirik
import { registry } from "@web/core/registry";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, onMounted, useState } from "@odoo/owl";
import { session } from "@web/session";
import { rpc } from "@web/core/network/rpc";

class QZPrintAction extends Component {
    setup() {
        // Lazım olan servisləri yükləyirik
        this.notification = useService("notification");
        this.action = useService("action");
        
        // Komponentimizin vəziyyəti
        this.state = useState({
            mode: 'preview',     // preview, printing, success, error
            receiptText: '',     // Çap ediləcək mətn
            errorMessage: ''     // Xəta mesajı
        });
        
        // Komponent yükləndikdə QZ Tray JS-ni yüklə
        onWillStart(async () => {
            await loadJS('https://cdn.jsdelivr.net/npm/qz-tray@2.2.0/qz-tray.js');
        });

        // DOM hazır olanda receipt hazırla
        onMounted(() => {
            this.prepareReceipt();
        });
    }

    /**
     * Python-dan gələn məlumatları receipt formatında hazırla
     */
    prepareReceipt() {
        const params = this.props.action.params || {};
        const name = params.name || 'Test Məhsul';
        const total = params.total || 0.0;

        // Receipt mətnini hazırla
        this.state.receiptText = `=== QZ YAZICI TEST ===
Ad: ${name}
Tutar: ${total} ${session.currency_symbol || 'AZN'}
-------------------------
Təşəkkür edirik!`;
    }

    /**
     * QZ Tray ilə çap et
     */
    async onPrintClick() {
        this.state.mode = 'printing';
        
        try {
            // Print job-u bazaya yaz (optional)
            await this.savePrintJob();
            
            // QZ Tray ilə çap et
            await this.connectAndPrint(this.state.receiptText);
            
            this.state.mode = 'success';
        } catch (error) {
            this.state.mode = 'error';
            this.state.errorMessage = error.message;
        }
    }

    /**
     * Browser-də çap et
     */
    async onBrowserPrintClick() {
        try {
            // Print job yaradırıq
            const printJob = await this.savePrintJob();
            
            // Yeni tab açıb çap et
            if (printJob) {
                window.open(`/print/job/${printJob}`, '_blank');
            }
        } catch (error) {
            this.notification.add('Browser çap xətası: ' + error.message, { type: 'danger' });
        }
    }

    /**
     * Dialog-u bağla
     */
    onCancelClick() {
        // Müxtəlif yollarla dialog-u bağlamağa çalış
        if (this.props.close) {
            this.props.close();
        } else if (this.props.onClose) {
            this.props.onClose();
        } else {
            // Action servisi ilə bağla
            this.action.doAction({ type: 'ir.actions.act_window_close' });
        }
    }

    /**
     * Print job-u bazaya yaz
     */
    async savePrintJob() {
        try {
            const params = this.props.action.params || {};
            const name = params.name || 'QZ Print Job';
            
            const printJob = await rpc({
                model: 'pos.print.job',
                method: 'create',
                args: [{
                    name: name,
                    content: this.state.receiptText,
                    status: 'pending'
                }]
            });
            
            return printJob;
        } catch (error) {
            console.error('Print job yaradılarkən xəta:', error);
            return null;
        }
    }

    /**
     * QZ Tray ilə çap et
     */
    async connectAndPrint(dataToPrint) {
        try {
            // QZ Tray yüklənmədisə, konsola çap et
            if (typeof qz === 'undefined') {
                console.log('QZ Tray yoxdur. Test rejimi:', dataToPrint);
                this.notification.add('Test rejimi: Konsola çap edildi (F12 > Console)', { type: 'success' });
                return;
            }

            // QZ Tray konfiqurasiyası - DÜZGÜNLƏŞDİRİLMİŞ
            qz.security.setSignaturePromise((toSign) => {
                return (resolve, reject) => {
                    // Test üçün sadəcə resolve edirik
                    resolve();
                };
            });

            // QZ Tray-ə qoşul
            if (!qz.websocket.isActive()) {
                await qz.websocket.connect();
            }
            
            // Printer tap
            const printer = await qz.printers.getDefault();
            if (!printer) {
                console.log('Printer yoxdur. Test rejimi:', dataToPrint);
                this.notification.add('Test rejimi: Printer tapılmadı', { type: 'warning' });
                return;
            }

            // Çap et
            const config = qz.configs.create(printer);
            const data = [{
                type: 'raw',
                format: 'plain',
                data: dataToPrint,
                options: { language: "epl", encoding: 'UTF-8' }
            }];

            await qz.print(config, data);
            this.notification.add('Çap edildi!', { type: 'success' });

        } catch (error) {
            console.error('QZ Tray xətası:', error);
            // Test rejimi üçün daha dostane xəta mesajı
            const errorMsg = error.message || error;
            console.log('Test rejimi - Çap ediləcək mətn:', dataToPrint);
            this.notification.add(`Test rejimi: ${errorMsg}`, {
                type: 'warning',
                title: 'Test Rejimi'
            });
            throw error;
        } finally {
            // Bağlantını kəs
            if (typeof qz !== 'undefined' && qz.websocket && qz.websocket.isActive()) {
                await qz.websocket.disconnect();
            }
        }
    }
}

// Template-i təyin et
QZPrintAction.template = "pos_qz_printer.QZPrintAction";

// Action-ı qeydiyyata al
registry.category("actions").add("print_qz_receipt", QZPrintAction);

/** @odoo-module */

import { registry } from "@web/core/registry";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, onMounted, useState } from "@odoo/owl";
import { session } from "@web/session";
import { rpc } from "@web/core/network/rpc";

class QZPrintAction extends Component {
    setup() {
        this.notification = useService("notification");
        this.action = useService("action");
        this.state = useState({
            mode: 'preview', // preview, printing, success, error
            receiptText: '',
            errorMessage: ''
        });
        
        onWillStart(async () => {
            // QZ Tray JS kitabxanasını yükləyirik
            await loadJS('https://cdn.jsdelivr.net/npm/qz-tray@2.2.0/qz-tray.js');
        });

        onMounted(() => {
            this.prepareReceipt();
        });
    }

    prepareReceipt() {
        // Python-dan göndərilən parametrləri alırıq
        const params = this.props.action.params || {};
        const name = params.name || 'N/A';
        const total = params.total || 0.0;

        this.state.receiptText = `=== QZ YAZICI TEST ===
Ad: ${name}
Tutar: ${total} ${session.currency_symbol || ''}
-------------------------
Tesekkur edirik!`;
    }

    async onPrintClick() {
        this.state.mode = 'printing';
        try {
            // Əvvəlcə print job yaradırıq
            await this.createPrintJob();
            
            // Sonra QZ Tray ilə çap etməyə çalışırıq
            await this._connectAndPrint(this.state.receiptText);
            this.state.mode = 'success';
        } catch (error) {
            this.state.mode = 'error';
            this.state.errorMessage = error.message;
        }
    }

    async createPrintJob() {
        /**
         * Print job yaradırıq ki, sonra browser ilə çap edə bilək
         */
        const params = this.props.action.params || {};
        const name = params.name || 'QZ Print Job';
        
        try {
            const printJob = await rpc({
                model: 'pos.print.job',
                method: 'create',
                args: [{
                    name: name,
                    content: this.state.receiptText,
                    content_type: 'receipt',
                    status: 'pending'
                }]
            });
            
            this.printJobId = printJob;
            console.log('Print job yaradıldı:', printJob);
            
        } catch (error) {
            console.error('Print job yaradılarkən xəta:', error);
            // Xəta olsa belə, çap etməyə davam edirik
        }
    }

    async onBrowserPrintClick() {
        /**
         * Browser-də yeni tab açıb çap et
         */
        if (this.printJobId) {
            window.open(`/print/job/${this.printJobId}`, '_blank');
        } else {
            // Print job yoxdursa, yaradırıq
            await this.createPrintJob();
            if (this.printJobId) {
                window.open(`/print/job/${this.printJobId}`, '_blank');
            }
        }
    }

    onCancelClick() {
        // Dialog-u bağla
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
     * QZ Tray-ə qoşulur və məlumatı çap edir.
     * @param {string} dataToPrint Çap ediləcək mətn
     * @private
     */
    async _connectAndPrint(dataToPrint) {
        try {
            // Test rejimi: QZ Tray yüklənməmişsə, sadəcə konsola çap et
            if (typeof qz === 'undefined') {
                console.log('QZ Tray mövcud deyil. Test rejimi:');
                console.log('Çap ediləcək mətn:', dataToPrint);
                this.notification.add('Test rejimi: Məlumat konsola çap edildi (F12 > Console-a bax)', { 
                    type: 'success' 
                });
                return;
            }

            qz.security.setSignaturePromise((toSign) => {
                // Production mühitində server tərəfində imzalama prosesi olmalıdır.
                // Test üçün birbaşa resolve edirik.
                return (resolve, reject) => resolve();
            });

            if (!qz.websocket.isActive()) {
                await qz.websocket.connect();
            }
            
            const printer = await qz.printers.getDefault();
            
            if (!printer) {
                // Printer yoxdursa, test rejimi
                console.log('Printer tapılmadı. Test rejimi:');
                console.log('Çap ediləcək mətn:', dataToPrint);
                this.notification.add('Test rejimi: Printer tapılmadı, məlumat konsola çap edildi', { 
                    type: 'warning' 
                });
                return;
            }

            const config = qz.configs.create(printer);
            const data = [{
                type: 'raw',
                format: 'plain',
                data: dataToPrint,
                options: { language: "epl", encoding: 'UTF-8' }
            }];

            await qz.print(config, data);
            this.notification.add('Məlumat printerə göndərildi.', { type: 'success' });

        } catch (err) {
            console.error("QZ Tray xətası:", err);
            // Test rejimi üçün daha dostane xəta mesajı
            const errorMsg = err.message || err;
            console.log('Test rejimi - Çap ediləcək mətn:', dataToPrint);
            this.notification.add(`Test rejimi: ${errorMsg}`, {
                type: 'warning',
                title: 'Test Rejimi'
            });
            throw err; // State-i error-a keçirmək üçün
        } finally {
            if (typeof qz !== 'undefined' && qz.websocket && qz.websocket.isActive()) {
                await qz.websocket.disconnect();
            }
        }
    }
}

// Komponent üçün şablon
QZPrintAction.template = "pos_qz_printer.QZPrintAction";

// Action-ı düzgün adla qeydiyyatdan keçiririk.
registry.category("actions").add("print_qz_receipt", QZPrintAction);

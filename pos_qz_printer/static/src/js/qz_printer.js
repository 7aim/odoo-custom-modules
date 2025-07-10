import { registry } from "@web/core/registry";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, onMounted, useState } from "@odoo/owl";
import { session } from "@web/session";

class QZPrintAction extends Component {
    setup() {
        this.notification = useService("notification");
        this.action = useService("action");
        this.state = useState({
            mode: 'preview',
            receiptText: '',
            errorMessage: ''
        });
        
        onWillStart(async () => {
            await loadJS('https://cdn.jsdelivr.net/npm/qz-tray@2.2.0/qz-tray.js');
        });

        onMounted(() => {
            this.prepareReceipt();
        });
    }

    prepareReceipt() {
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
            await this._connectAndPrint(this.state.receiptText);
            this.state.mode = 'success';
        } catch (error) {
            this.state.mode = 'error';
            this.state.errorMessage = error.message;
        }
    }

    onCancelClick() {
        window.history.back();
        /*
        if (this.props.close) {
            this.props.close();
        } else {
            this.action.doAction({ type: 'ir.actions.act_window_close' });
        }
        */
    }

    /**
     * QZ Tray çap funksiyası
     */
    async _connectAndPrint(dataToPrint) {
        try {
            // QZ Tray yüklənib-yüklənmədiyini yoxla
            if (typeof qz === 'undefined') {
                throw new Error('QZ Tray programı yüklənməyib. Zəhmət olmasa QZ Tray-i yükləyib işə salın.');
            }

            // QZ Tray signature
            qz.security.setSignaturePromise((toSign) => {
                return (resolve, reject) => resolve();
            });

            // QZ Tray-ə qoşulmağa çalış
            if (!qz.websocket.isActive()) {
                this.notification.add('QZ Tray-ə qoşulur...', { type: 'info' });
                await qz.websocket.connect();
                this.notification.add('QZ Tray-ə qoşuldu!', { type: 'success' });
            }
            
            // Printer-ləri tap
            const printers = await qz.printers.find();
            this.notification.add(`${printers.length} printer tapıldı`, { type: 'info' });
            
            if (printers.length === 0) {
                throw new Error('Heç bir printer tapılmadı. Printer qoşulu olduğundan əmin olun.');
            }
            
            // Default printer al
            const printer = await qz.printers.getDefault();
            if (!printer) {
                throw new Error('Default printer təyin edilməyib.');
            }
            
            this.notification.add(`Printer: ${printer}`, { type: 'info' });

            // Çap et
            const config = qz.configs.create(printer);
            const data = [{
                type: 'raw',
                format: 'plain',
                data: dataToPrint
            }];

            await qz.print(config, data);
            this.notification.add(`✅ Çap uğurla tamamlandı! Printer: ${printer}`, { type: 'success' });

        } catch (err) {
            const errorMsg = err.message || err;
            this.notification.add(`❌ QZ Tray Xətası: ${errorMsg}`, { type: 'danger' });
            throw err;
        } finally {
            // QZ Tray bağlantısını kəs
            if (typeof qz !== 'undefined' && qz.websocket && qz.websocket.isActive()) {
                await qz.websocket.disconnect();
                this.notification.add('QZ Tray bağlantısı kəsildi', { type: 'info' });
            }
        }
    }
}

QZPrintAction.template = "pos_qz_printer.QZPrintAction";
registry.category("actions").add("print_qz_receipt", QZPrintAction);
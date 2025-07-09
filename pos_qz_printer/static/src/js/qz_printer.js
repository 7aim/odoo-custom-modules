/** @odoo-module */

import { registry } from "@web/core/registry";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart } from "@odoo/owl";
import { BlockUI } from "@web/core/ui/block_ui";
import { session } from "@web/session";

class QZPrintAction extends Component {
    setup() {
        super.setup();
        this.notification = useService("notification");
        this.action = useService("action");
        this.rpc = useService("rpc");

        onWillStart(async () => {
            // QZ Tray JS kitabxanasını birbaşa CDN-dən yükləyirik.
            await loadJS('https://cdn.jsdelivr.net/npm/qz-tray@2.2.0/qz-tray.js');
        });
    }

    /**
     * Komponent DOM-a əlavə edildikdən sonra bu funksiya işə düşür.
     */
    async mounted() {
        // Python-dan göndərilən parametrləri alırıq
        const params = this.props.action.params || {};
        const name = params.name || 'N/A';
        const total = params.total || 0.0;

        const receiptText = `
=== QZ YAZICI TEST ===
Ad: ${name}
Tutar: ${total} ${session.currency_symbol || ''}
-------------------------
Tesekkur edirik!\n\n`;

        // QZ Tray-ə qoşulub çap etmə funksiyasını çağırırıq
        BlockUI();
        try {
            await this._connectAndPrint(receiptText);
        } finally {
            // Pəncərəni bağlayırıq və bloku aradan qaldırırıq
            this.props.onClose();
        }
    }

    /**
     * QZ Tray-ə qoşulur və məlumatı çap edir.
     * @param {string} dataToPrint Çap ediləcək mətn
     * @private
     */
    async _connectAndPrint(dataToPrint) {
        try {
            if (typeof qz === 'undefined') {
                throw new Error('QZ Tray JavaScript kitabxanası yüklənmədi.');
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
                throw new Error("Sistemdə varsayılan (default) printer tapılmadı.");
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
            this.notification.add(`Printerə qoşularkən xəta baş verdi: ${err.message || err}`, {
                type: 'danger',
                title: 'QZ Tray Xətası'
            });
        } finally {
            if (qz && qz.websocket.isActive()) {
                await qz.websocket.disconnect();
            }
        }
    }
}

// Komponent üçün şablon
QZPrintAction.template = "pos_qz_printer.QZPrintAction";

// Action-ı düzgün adla qeydiyyatdan keçiririk.
registry.category("actions").add("print_qz_receipt", QZPrintAction);
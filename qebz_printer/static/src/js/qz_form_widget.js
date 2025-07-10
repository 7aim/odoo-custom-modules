import { registry } from "@web/core/registry";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onWillStart } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { session } from "@web/session";

export class QZFormWidget extends Component {
    setup() {
        this.notification = useService("notification");
        this.state = useState({
            isPrinting: false,
            errorMessage: null, // Xəta mesajları üçün
        });

        onWillStart(async () => {
            // QZ Tray kitabxanasını bir dəfə yükləyirik
            await loadJS('https://cdn.jsdelivr.net/npm/qz-tray@2.2.0/qz-tray.js');
        });
    }

    // Formdakı 'name' və 'total' dəyişdikcə bu mətn avtomatik yenilənəcək
    get receiptText() {
        const record = this.props.record.data;
        const name = record.name || 'N/A';
        const total = record.total || 0.0;
        const currency = session.currency_symbol || '';

        return `=== QZ YAZICI TEST ===
Ad: ${name}
Tutar: ${total} ${currency}
-------------------------
Tesekkur edirik!`;
    }

    async onPrintClick() {
        this.state.isPrinting = true;
        this.state.errorMessage = null; // Əvvəlki xətanı təmizlə
        try {
            await this._connectAndPrint(this.receiptText);
            // Uğurlu bildiriş _connectAndPrint içində göstərilir
        } catch (error) {
            this.state.errorMessage = error.message || "Bilinməyən bir xəta baş verdi.";
            // Xəta bildirişi _connectAndPrint içində göstərilir
        } finally {
            this.state.isPrinting = false;
            window.history.back();
        }
    }

 
     //  QZ Tray çap funksiyası ( yoxlamalarla birlikde )
    async _connectAndPrint(dataToPrint) {
        try {
            // 1. QZ Tray yüklənib-yüklənmədiyini yoxla
            if (typeof qz === 'undefined') {
                throw new Error('QZ Tray proqramı yüklənməyib. Zəhmət olmasa QZ Tray-i yükləyib işə salın.');
            }

            // 2. Signature (Bu hissə boş qala bilər, development üçün)
            qz.security.setSignaturePromise((toSign) => resolve => resolve());

            // 3. QZ Tray-ə qoşulmağa çalış
            if (!qz.websocket.isActive()) {
                this.notification.add('QZ Tray-ə qoşulur...', { type: 'info' });
                await qz.websocket.connect();
                this.notification.add('QZ Tray-ə uğurla qoşuldu!', { type: 'success' });
            }
            
            // 4. Printer-ləri tap
            const printers = await qz.printers.find();
            this.notification.add(`${printers.length} printer tapıldı.`, { type: 'info' });
            
            if (printers.length === 0) {
                throw new Error('Heç bir printer tapılmadı. Printerin qoşulu olduğundan əmin olun.');
            }
            
            // 5. Default printeri al
            const printer = await qz.printers.getDefault();
            if (!printer) {
                throw new Error('Default (əsas) printer təyin edilməyib.');
            }
            
            this.notification.add(`Əsas printer: ${printer}`, { type: 'info', sticky: true });

            // 6. Çap et
            const config = qz.configs.create(printer);
            const data = [{
                type: 'raw',
                format: 'plain',
                data: dataToPrint
            }];

            await qz.print(config, data);
            this.notification.add(`✅ Çap uğurla tamamlandı! Printer: ${printer}`, { type: 'success', sticky: true });

        } catch (err) {
            const errorMsg = err.message || err.toString();
            this.notification.add(`❌ QZ Tray Xətası: ${errorMsg}`, { type: 'danger', sticky: true });
            throw err; // Xətanı yuxarıdakı onPrintClick-ə göndəririk
        } finally {
            // 7. QZ Tray bağlantısını kəs (hər dəfə kəsmək daha stabildir)
            if (typeof qz !== 'undefined' && qz.websocket && qz.websocket.isActive()) {
                await qz.websocket.disconnect();
                this.notification.add('QZ Tray bağlantısı kəsildi.', { type: 'info' });
            }
        }
    }
}

// Widget-in Odoo üçün tərifi
QZFormWidget.props = { ...standardFieldProps };
QZFormWidget.template = "pos_qz_printer.QZFormWidget";
registry.category("fields").add("qz_form_printer", { component: QZFormWidget });
odoo.define('pos_qz_printer.action', function (require) {
"use strict";

const AbstractAction = require('web.AbstractAction');
const core = require('web.core');
const { loadJS } = require('@web/core/assets');
const { useService } = require("@web/core/utils/hooks");
const { onWillStart } = require("@odoo/owl");

const QZPrintAction = AbstractAction.extend({
    // Bu, Odoo-nun bildiriş sistemini istifadə etmək üçün lazımdır
    hasControlPanel: false,

    /**
     * Odoo 16-da xarici kitabxanaları yükləmək üçün ən yaxşı üsul
     * `willStart` lifecycle metodunu istifadə etməkdir.
     */
    willStart: function () {
        // QZ Tray JS kitabxanasını birbaşa CDN-dən yükləyirik.
        // Bu, kitabxananı manual olaraq qovluğa atmaqdan daha asandır.
        return Promise.all([
            this._super.apply(this, arguments),
            loadJS('https://cdn.jsdelivr.net/npm/qz-tray@2.2.0/qz-tray.js')
        ]);
    },

    /**
     * Action işə düşdükdə bu funksiya çağırılır.
     */
    start: function () {
        this._super.apply(this, arguments);
        // Python-dan göndərilən parametrləri alırıq
        const params = this.options && this.options.params || {};
        const name = params.name || 'N/A';
        const total = params.total || 0.0;

        const receiptText = `
    === QZ YAZICI TEST ===
Ad: ${name}
Tutar: ${total} AZN
-------------------------
Teşekkür ederiz!\n\n`;

        // QZ Tray-ə qoşulub çap etmə funksiyasını çağırırıq
        this._connectAndPrint(receiptText);

        // Bu action öz işini arxa planda gördüyü üçün
        // dərhal pəncərəni bağlaya bilərik.
        return this.do_action({ type: 'ir.actions.act_window_close' });
    },

    /**
     * QZ Tray-ə qoşulur və məlumatı çap edir.
     * @param {string} dataToPrint Çap ediləcək mətn
     * @private
     */
    _connectAndPrint: function (dataToPrint) {
        // QZ Tray kitabxanasının yüklənib-yüklənmədiyini yoxlayırıq
        if (typeof qz === 'undefined') {
            this.displayNotification({
                type: 'danger',
                title: 'Xəta',
                message: 'QZ Tray JavaScript kitabxanası yüklənmədi.'
            });
            return;
        }

        // QZ Tray ilə təhlükəsiz bağlantı üçün bu addım vacibdir.
        // Production mühitində server tərəfində imzalama prosesi olmalıdır.
        // https://qz.io/wiki/signing-messages
        qz.security.setSignaturePromise((toSign) => {
            // İndi üçün bu hissəni boş saxlayırıq, ancaq production üçün vacibdir.
            return (resolve, reject) => {
                // Burada serverə müraciət edib imza almalısınız.
                // Test üçün birbaşa resolve edirik.
                resolve();
            };
        });

        qz.websocket.connect().then(() => {
            console.log("QZ Tray-ə uğurla qoşuldu!");
            // Varsayılan (default) printeri tapırıq
            return qz.printers.getDefault();
        }).then((printer) => {
            if (!printer) {
                throw new Error("Sistemdə varsayılan (default) printer tapılmadı.");
            }
            console.log("Default printer:", printer);
            const config = qz.configs.create(printer);
            const data = [{
                type: 'raw',
                format: 'plain',
                data: dataToPrint,
                options: { language: "epl", encoding: 'UTF-8' } // Printer dilini və kodlaşdırmanı təyin edin
            }];
            return qz.print(config, data);
        }).then(() => {
            console.log("Çap əməliyyatı uğurla göndərildi.");
            this.displayNotification({
                type: 'success',
                title: 'Uğurlu',
                message: 'Məlumat printerə göndərildi.'
            });
            // Qoşulunu kəsirik
            return qz.websocket.disconnect();
        }).catch(err => {
            console.error("QZ Tray xətası:", err);
            // `alert()` yerinə Odoo-nun öz bildiriş sistemini istifadə edirik.
            this.displayNotification({
                type: 'danger',
                title: 'QZ Tray Xətası',
                message: `Printerə qoşularkən xəta baş verdi: ${err.message || err}`
            });
        });
    },
});

// Action-ı düzgün adla qeydiyyatdan keçiririk.
core.action_registry.add('print_qz_receipt', QZPrintAction);

return QZPrintAction;

});

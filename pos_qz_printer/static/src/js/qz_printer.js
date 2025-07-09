odoo.define('custom_qz_printer.qz_print', function (require) {
    const AbstractAction = require('web.AbstractAction');
    const core = require('web.core');

    const QZPrintAction = AbstractAction.extend({
        start: function () {
            const params = this.options.params;

            const receiptText = `
        === QZ YAZICI TEST ===
Ad: ${params.name}
Tutar: ${params.total}₺
-------------------------
Teşekkür ederiz!\n\n`;

            // QZ Tray bağlantısı
            qz.websocket.connect().then(() => {
                const config = qz.configs.create(null); // Varsayılan yazıcı
                const data = [{ type: 'raw', format: 'plain', data: receiptText }];
                return qz.print(config, data);
            }).catch(err => {
                console.error("Yazıcı bağlantı hatası:", err);
                alert("QZ Tray bağlantı hatası: " + err);
            });

            return Promise.resolve();
        }
    });

    core.action_registry.add('print_qz_receipt', QZPrintAction);
});

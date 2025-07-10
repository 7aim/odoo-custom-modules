odoo.define('pos_qz_printer.pos_integration', function (require) {
    'use strict';

    const { PaymentScreen } = require('point_of_sale.PaymentScreen');
    const { _t } = require('web.core');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const rpc = require('web.rpc');

    const PosQZPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            constructor() {
                super(...arguments);
                useListener('click-validated', this._onOrderValidated);
            }

            async _onOrderValidated() {
                const order = this.currentOrder;
                const orderId = order.backendId; // Serverdəki ID

                if (orderId) {
                    try {
                        // Addım 1-də yaratdığımız Python metodunu çağırırıq
                        const receiptContent = await rpc.query({
                            model: 'pos.print.job',
                            method: 'get_receipt_content',
                            args: [orderId],
                        });

                        // Mövcud çap məntiqinizi burada çağırın
                        await this._printWithQZTray(receiptContent);

                    } catch (error) {
                        console.error('QZ Printer Error:', error);
                        this.showPopup('ErrorPopup', {
                            title: _t('Printer Error'),
                            body: _t('Could not print the receipt via QZ Tray.'),
                        });
                    }
                }
            }

            // Mövcud _connectAndPrint funksiyanızı buraya köçürün
            async _printWithQZTray(dataToPrint) {
                // ... qz.websocket.connect(), qz.print() və s. məntiqi ...
                // Bu məntiqi qz_form_widget.js-dən götürə bilərsiniz
                // Səhvləri və bildirişləri göstərmək üçün this.showPopup istifadə edin
            }
        };

    Registries.Component.extend(PaymentScreen, PosQZPaymentScreen);

    return PaymentScreen;
});
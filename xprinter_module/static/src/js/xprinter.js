odoo.define('xprinter_module.XPrinterIntegration', function(require) {
    'use strict';

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');

    const XPrinterPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            async validateOrder(isForceValidate) {
                // Çap göndərişi
                try {
                    await fetch('http://localhost:5000/print', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            text: 'Sizin POS çəkiniz: Məhsul və qiymətlər'
                        }),
                    });
                    console.log('Çap uğurla göndərildi');
                } catch (err) {
                    console.error('Printerə göndərmə xətası:', err);
                }

                // Əsas validate funksiyasını çağır
                return super.validateOrder(isForceValidate);
            }
        };

    Registries.Component.extend(PaymentScreen, XPrinterPaymentScreen);

    return PaymentScreen;
});

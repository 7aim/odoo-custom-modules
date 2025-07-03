/** @odoo-module */

import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

// Odoo-nun standart 'Order' modelinə patch tətbiq edirik
patch(Order.prototype, {
    // Çap üçün məlumatları hazırlayan funksiyanı genişləndiririk
    export_for_printing() {
        // Orijinal funksiyanın nəticəsini alırıq
        const result = super.export_for_printing(...arguments);
        const partner = this.get_partner();

        // Əgər müştəri seçilibsə və onun borc məlumatı varsa, nəticəyə əlavə edirik
        if (partner && partner.customer_old_due) {
            result.customer_old_due = partner.customer_old_due;
        } else {
            result.customer_old_due = 0;
        }

        return result;
    },
});
/** @odoo-module **/

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";
import { CustomOrderReceipt } from "@pos_receipt_customisation/js/CustomOrderReceipt";

patch(PosStore.prototype, {
    async printReceipt({
        basic = false,
        order = this.get_order(),
        printBillActionTriggered = false,
    } = {}) {
        await this.printer.print(
            CustomOrderReceipt, {
                data: this.orderExportForPrinting(order),
                formatCurrency: this.env.utils.formatCurrency,
                basic_receipt: basic,
            }, { webPrintFallback: true }
        );
        if (!printBillActionTriggered) {
            const nbrPrint = order.nb_print;
            await this.data.write("pos.order", [order.id], { nb_print: nbrPrint + 1 });
        }
        return true;
    }
});
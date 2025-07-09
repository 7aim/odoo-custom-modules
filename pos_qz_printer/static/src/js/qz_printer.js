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
            console.log('Print job yaradılır:', {
                name: name,
                content: this.state.receiptText,
                content_type: 'receipt',
                status: 'pending'
            });
            
            // RPC çağrısını daha safe formada edirik
            const printJob = await rpc("/web/dataset/call_kw", {
                model: 'pos.print.job',
                method: 'create',
                args: [{
                    name: name,
                    content: this.state.receiptText,
                    content_type: 'receipt',
                    status: 'pending'
                }],
                kwargs: {}
            });
            
            this.printJobId = printJob;
            console.log('Print job yaradıldı:', printJob);
            
        } catch (error) {
            console.error('Print job yaradılarkən xəta:', error);
            this.notification.add(`Print job yaradılarkən xəta: ${error.message}`, { 
                type: 'danger',
                title: 'Database Xətası'
            });
            throw error;
        }
    }

    async onBrowserPrintClick() {
        /**
         * Browser-də yeni tab açıb çap et
         */
        console.log('Browser print düyməsi basıldı');
        try {
            if (this.printJobId) {
                console.log('Print job mövcuddur:', this.printJobId);
                window.open(`/print/job/${this.printJobId}`, '_blank');
            } else {
                console.log('Print job yoxdur, yaradılacaq');
                // Print job yoxdursa, yaradırıq
                this.notification.add('Print job yaradılır...', { type: 'info' });
                try {
                    await this.createPrintJob();
                    if (this.printJobId) {
                        console.log('Yeni print job yaradıldı:', this.printJobId);
                        window.open(`/print/job/${this.printJobId}`, '_blank');
                    } else {
                        throw new Error('Print job yaradıla bilmədi');
                    }
                } catch (rpcError) {
                    // RPC işləməsə, sadə HTML print açaq
                    console.error('RPC xətası, sadə HTML print açılır:', rpcError);
                    this.openSimpleHTMLPrint();
                }
            }
        } catch (error) {
            console.error('Browser print xətası:', error);
            this.notification.add(`Browser print xətası: ${error.message}`, { 
                type: 'danger',
                title: 'Xəta'
            });
            // Son çarə - sadə HTML print
            this.openSimpleHTMLPrint();
        }
    }

    openSimpleHTMLPrint() {
        /**
         * Sadə HTML print - database işləməsə belə
         */
        const htmlContent = `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>QZ Print</title>
            <style>
                body { 
                    font-family: 'Courier New', monospace; 
                    font-size: 12px; 
                    margin: 20px;
                    background: white;
                }
                .receipt { 
                    max-width: 300px; 
                    margin: 0 auto; 
                    padding: 20px;
                    border: 1px solid #ddd;
                    background: white;
                }
                .no-print { 
                    margin: 20px 0;
                    text-align: center;
                }
                .print-btn {
                    background: #007bff;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    cursor: pointer;
                    font-size: 14px;
                    margin: 0 10px;
                }
                @media print {
                    .no-print { display: none; }
                    body { margin: 0; }
                    .receipt { border: none; max-width: none; }
                }
            </style>
        </head>
        <body>
            <div class="no-print">
                <button class="print-btn" onclick="window.print()">🖨️ Çap Et</button>
                <button class="print-btn" onclick="window.close()">❌ Bağla</button>
            </div>
            
            <div class="receipt">
                <pre>${this.state.receiptText}</pre>
            </div>
        </body>
        </html>
        `;
        
        const printWindow = window.open('', '_blank');
        printWindow.document.write(htmlContent);
        printWindow.document.close();
    }

    onCancelClick() {
        console.log('Tamam düyməsi basıldı');
        console.log('Props:', this.props);
        console.log('Env:', this.env);
        
        // Dialog-u bağla - müxtəlif üsulları sınayırıq
        try {
            // 1. Odoo 17+ üçün yeni üsul
            if (this.env && this.env.services && this.env.services.dialog) {
                console.log('Dialog service istifadə edilir');
                this.env.services.dialog.closeAll();
                return;
            }
            
            // 2. Props-dan gələn close funksiyası
            if (this.props.close) {
                console.log('props.close istifadə edilir');
                this.props.close();
                return;
            }
            
            // 3. onClose callback
            if (this.props.onClose) {
                console.log('props.onClose istifadə edilir');
                this.props.onClose();
                return;
            }
            
            // 4. Action service
            if (this.action) {
                console.log('action.doAction istifadə edilir');
                this.action.doAction({ type: 'ir.actions.act_window_close' });
                return;
            }
            
            // 5. History back
            if (window.history && window.history.length > 1) {
                console.log('History back istifadə edilir');
                window.history.back();
                return;
            }
            
            // 6. Son çarə - pəncərəni bağla
            console.log('window.close istifadə edilir');
            window.close();
            
        } catch (error) {
            console.error('Dialog bağlanarkən xəta:', error);
            // Force close
            if (window.parent && window.parent !== window) {
                window.parent.postMessage({ action: 'close_dialog' }, '*');
            } else {
                window.close();
            }
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
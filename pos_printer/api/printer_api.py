from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import win32print
import win32ui
import win32con
from typing import List, Dict
import uvicorn
from datetime import datetime

app = FastAPI(title="Custom POS Printer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PrinterService:
    @staticmethod
    def get_printers() -> List[Dict]:
        """Sistemdə mövcud printerləri tapır"""
        printers = []
        for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL):
            printers.append({
                "name": printer[2],
                "status": "ready",
                "type": "local"
            })
        return printers
    
    @staticmethod
    def print_text_advanced(printer_name: str, text: str) -> bool:
        """Təkmilləşdirilmiş mətn çapı - sətir sətir formatlanmış"""
        try:
            hprinter = win32print.OpenPrinter(printer_name)
            try:
                hdc = win32ui.CreateDC()
                hdc.CreatePrinterDC(printer_name)
                
                # Font yaradın
                font_dict = {
                    'name': 'Courier New',  # Monospace font
                    'height': 200,  # Font ölçüsü
                    'weight': 400,  # Normal qalınlıq
                }
                font = win32ui.CreateFont(font_dict)
                old_font = hdc.SelectObject(font)
                
                hdc.StartDoc("POS Receipt")
                hdc.StartPage()
                
                # Mətn sətirlərinə bölün
                lines = text.split('\n')
                y_pos = 100  # Başlanğıc Y pozisiyası
                line_height = 250  # Sətir yüksəkliyi
                
                for line in lines:
                    if line.strip():  # Boş sətirləri keç
                        hdc.TextOut(100, y_pos, line)
                    y_pos += line_height
                
                hdc.SelectObject(old_font)
                hdc.EndPage()
                hdc.EndDoc()
                return True
                
            finally:
                win32print.ClosePrinter(hprinter)
        except Exception as e:
            print(f"Print error: {e}")
            return False

    @staticmethod
    def print_receipt_format(printer_name: str, content: str) -> bool:
        """Qəbz formatında çap - POS üçün optimized"""
        try:
            # Raw printer data göndər
            hprinter = win32print.OpenPrinter(printer_name)
            try:
                # ESC/POS komandları ilə format
                raw_data = content.encode('cp1252', errors='ignore')  # Windows encoding
                
                job_id = win32print.StartDocPrinter(hprinter, 1, ("Receipt", None, "RAW"))
                win32print.StartPagePrinter(hprinter)
                win32print.WritePrinter(hprinter, raw_data)
                win32print.EndPagePrinter(hprinter)
                win32print.EndDocPrinter(hprinter)
                return True
                
            finally:
                win32print.ClosePrinter(hprinter)
        except Exception as e:
            print(f"Receipt print error: {e}")
            return False

@app.get("/printers")
async def get_printers():
    """Printerləri qaytarır"""
    try:
        printers = PrinterService.get_printers()
        return {"status": "success", "printers": printers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/print")
async def print_receipt(data: dict):
    """Qəbz çap edir - təkmilləşdirilmiş format"""
    try:
        printer_name = data.get("printer")
        content = data.get("data", "")
        print_type = data.get("type", "receipt")  # receipt, document, raw
        
        if not printer_name:
            raise HTTPException(status_code=400, detail="Printer name required")
        
        # Çap növünə görə müxtəlif metodlar
        if print_type == "receipt":
            success = PrinterService.print_receipt_format(printer_name, content)
        else:
            success = PrinterService.print_text_advanced(printer_name, content)
        
        if success:
            return {"status": "success", "message": "Print job completed"}
        else:
            raise HTTPException(status_code=500, detail="Print failed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/print/formatted")
async def print_formatted_receipt(data: dict):
    """Formatlanmış qəbz çapı - ESC/POS komandaları ilə"""
    try:
        printer_name = data.get("printer")
        receipt_data = data.get("receipt", {})
        
        if not printer_name:
            raise HTTPException(status_code=400, detail="Printer name required")
        
        # ESC/POS formatlanmış mətn hazırla
        formatted_text = format_receipt_escpos(receipt_data)
        
        success = PrinterService.print_receipt_format(printer_name, formatted_text)
        
        if success:
            return {"status": "success", "message": "Formatted receipt printed"}
        else:
            raise HTTPException(status_code=500, detail="Print failed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def format_receipt_escpos(receipt_data):
    """ESC/POS komandaları ilə qəbz formatla"""
    ESC = chr(27)
    
    # ESC/POS komandaları
    INIT = ESC + "@"  # Initialize
    BOLD_ON = ESC + "E" + chr(1)  # Bold ON
    BOLD_OFF = ESC + "E" + chr(0)  # Bold OFF
    CENTER = ESC + "a" + chr(1)  # Center align
    LEFT = ESC + "a" + chr(0)  # Left align
    CUT = ESC + "m"  # Cut paper
    
    formatted = INIT
    
    # Header
    formatted += CENTER + BOLD_ON
    formatted += receipt_data.get("shop_name", "MAĞAZA ADI") + "\n"
    formatted += BOLD_OFF
    formatted += receipt_data.get("address", "Ünvan məlumatı") + "\n"
    formatted += "Tel: " + receipt_data.get("phone", "012-345-67-89") + "\n"
    formatted += "-" * 32 + "\n"
    
    # Date/Time
    formatted += LEFT
    formatted += f"Tarix: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
    formatted += f"Qəbz №: {receipt_data.get('receipt_no', '001')}\n"
    formatted += "-" * 32 + "\n"
    
    # Items
    items = receipt_data.get("items", [])
    for item in items:
        name = item.get("name", "Məhsul")[:20]  # 20 simvol limit
        qty = item.get("qty", 1)
        price = item.get("price", 0)
        total = qty * price
        
        formatted += f"{name:<20} {qty:>3}x{price:>6.2f}\n"
        formatted += f"{'':>20} = {total:>8.2f}\n"
    
    formatted += "-" * 32 + "\n"
    
    # Total
    formatted += BOLD_ON
    total_amount = receipt_data.get("total", 0)
    formatted += f"{'CƏMİ:':<20} {total_amount:>10.2f} AZN\n"
    formatted += BOLD_OFF
    
    # Footer
    formatted += "\n" + CENTER
    formatted += "Təşəkkür edirik!\n"
    formatted += "Yenidən gələcəyinizi gözləyirik\n"
    formatted += "\n\n" + CUT
    
    return formatted

@app.get("/status")
async def get_status():
    """API statusu"""
    return {"status": "running", "version": "1.0.0"}

@app.get("/test")
async def test_endpoint():
    """Test endpoint"""
    return {
        "message": "API is working!",
        "timestamp": str(datetime.now()),
        "printers_count": len(PrinterService.get_printers())
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8765)
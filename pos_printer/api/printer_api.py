from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import win32print
import win32ui
import win32con
from typing import List, Dict
import json
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
    def print_text(printer_name: str, text: str) -> bool:
        """Mətn çap edir"""
        try:
            hprinter = win32print.OpenPrinter(printer_name)
            try:
                hdc = win32ui.CreateDC()
                hdc.CreatePrinterDC(printer_name)
                hdc.StartDoc("POS Receipt")
                hdc.StartPage()
                
                # Mətn çap et
                hdc.TextOut(50, 50, text)
                
                hdc.EndPage()
                hdc.EndDoc()
                return True
            finally:
                win32print.ClosePrinter(hprinter)
        except Exception as e:
            print(f"Print error: {e}")
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
    """Qəbz çap edir"""
    try:
        printer_name = data.get("printer")
        content = data.get("data", "")
        
        if not printer_name:
            raise HTTPException(status_code=400, detail="Printer name required")
        
        success = PrinterService.print_text(printer_name, content)
        
        if success:
            return {"status": "success", "message": "Print job completed"}
        else:
            raise HTTPException(status_code=500, detail="Print failed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
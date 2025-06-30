from escpos.printer import Usb

# Bunları printer modelinə görə dəyiş (lsusb ilə baxmaq olar)
printer = Usb(0x0416, 0x5011)  # VendorID və ProductID

printer.text("Salam Sahib bəy!\n")
printer.cut()

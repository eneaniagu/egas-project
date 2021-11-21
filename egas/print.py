from win32printing import Printer

font = {
    "height": 12,
}
with Printer(linegap=1) as printer:
    printer.text("attached to the laptop.", font_config=font)
    printer.text(" and then send the PDF to the thermal printer attached to the laptop.", font_config=font)
    printer.text("title3", font_config=font)
    printer.text("title4", font_config=font)
    printer.new_page()
    printer.text("title5", font_config=font)
    printer.text("title6", font_config=font)
    printer.text("title7", font_config=font)
    printer.text("title8", font_config=font)
import badger2040
import qrcode
import pngdec

display = badger2040.Badger2040()
code = qrcode.QRCode()

def measure_qr_code(size, code):
    w, h = code.get_size()
    module_size = int(size / w)
    return module_size * w, module_size

def draw_qr_code(ox, oy, size, code):
    size, module_size = measure_qr_code(size, code)
    display.set_pen(15)
    display.rectangle(ox, oy, size, size)
    display.set_pen(0)
    for x in range(size):
        for y in range(size):
            if code.get_module(x, y):
                display.rectangle(ox + x * module_size, oy + y * module_size, module_size, module_size)

display.led(128)
codetext = open("/evan/content.txt", "r")
try:
    lines = codetext.read().strip().split("\n")
    code_text = lines.pop(0)
    title_text = lines.pop(0)
    detail_text = lines

    # Clear the Display
    display.set_pen(15)  # Change this to 0 if a white background is used
    display.clear()
    display.set_pen(0)

    code.set_text(code_text)
    size, _ = measure_qr_code(128, code)
    left = top = int((badger2040.HEIGHT / 2) - (size / 2))
    draw_qr_code(left, top, 128, code)

    display.set_font("bitmap8")
    left = 128 + 5
    top = 82
    display.text(title_text, left, top, badger2040.WIDTH, 2)
    top += 18

    for line in detail_text:
        display.text(line, left, top, badger2040.WIDTH, 1)
        top += 10
    
    png = pngdec.PNG(display.display)
    png.open_file("/evan/logo.png")
    png.decode(left + 22, 0)

    display.update()
finally:
    codetext.close()

while True:
    display.keepalive()
    display.halt()

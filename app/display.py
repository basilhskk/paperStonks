from PIL import Image, ImageDraw, ImageFont
from datetime import datetime


# Import your Waveshare driver by model name from config
# Example for 2.13" v4:
from TP_lib import epd2in13_V4 as epd_driver

FONT_REG = ImageFont.truetype("fonts/Inter-Regular.ttf", 18)
FONT_BIG = ImageFont.truetype("fonts/Inter-Bold.ttf", 40)
FONT_SM = ImageFont.truetype("fonts/Inter-Regular.ttf", 14)


class Display:
    def __init__(self, rotation=0):
        self.epd = epd_driver.EPD()
        # Initialize with full update mode
        self.epd.init(self.epd.FULL_UPDATE)
        self.rotation = rotation
        self.width, self.height = self.epd.height, self.epd.width  # note swap
        self.padding = 4

    def clear(self):
        self.epd.init(self.epd.FULL_UPDATE)
        self.epd.Clear(0xFF)

    def header(self,imageDraw,label):
        imageDraw.text((6, 4), label, font=FONT_REG, fill=0)
        ts = datetime.now()
        time_text = ts.strftime('%H:%M')
        text_w, text_h = imageDraw.textsize(time_text, font=FONT_SM,fill=0)
        x = self.width - text_w - self.padding  # 4px padding from right edge
        y = self.padding
        imageDraw.text((x, y), time_text, font=FONT_SM, fill=0)

    def draw_ticker(self, label, price, change_pct, ts, invert_down=True):
        img = Image.new('1', (self.width, self.height), 255)
        d = ImageDraw.Draw(img)

        # Header
        self.header(d,label)

        # Price
        price_txt = f"{price:,.2f}" if isinstance(price, (int, float)) else str(price)
        w, h = d.textsize(price_txt, font=FONT_BIG)
        d.text(((self.width - w) // 2, 30), price_txt, font=FONT_BIG, fill=0)

        # Change
        arrow = "▲" if change_pct >= 0 else "▼"
        change_txt = f"{arrow} {change_pct:+.2f}%"
        fill = 0
        d.text(((self.width - d.textsize(change_txt, FONT_REG)[0]) // 2, 80),
               change_txt, font=FONT_REG, fill=fill)

        # Update with partial refresh to avoid flicker
        self.epd.init(self.epd.PART_UPDATE)
        self.epd.display(self.epd.getbuffer(img))

    def sleep(self):
        self.epd.sleep()

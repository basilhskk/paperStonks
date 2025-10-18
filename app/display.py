from PIL import Image, ImageDraw, ImageFont
from datetime import datetime


# Import your Waveshare driver by model name from config
# Example for 2.13" v4:
from TP_lib import epd2in13_V4 as epd_driver

FONT_REG = ImageFont.truetype("fonts/Inter-Regular.ttf", 18)
FONT_BIG = ImageFont.truetype("fonts/Inter-Bold.ttf", 40)
FONT_SM = ImageFont.truetype("fonts/Inter-Regular.ttf", 14)


def text_wh(draw, text, font):
    try:
        l,t,r,b = draw.textbbox((0,0), text, font=font)
        return r-l, b-t
    except AttributeError:
        return draw.textsize(text, font=font)

class Display:
    def __init__(self, rotation=0):
        self.epd = epd_driver.EPD()
        self.epd.init(self.epd.FULL_UPDATE)
        self.rotation = rotation
        self.width, self.height = self.epd.height, self.epd.width
        self.pad = 6
        self.partial_count = 0

    def header(self, d, label):
        # Label (left)
        d.text((self.pad, self.pad), label, font=FONT_REG, fill=0)
        # Time (right)
        ts = datetime.now()
        time_text = ts.strftime('%H:%M')
        tw, th = text_wh(d, time_text, FONT_SM)
        x = self.width - tw - self.pad
        d.text((x, self.pad), time_text, font=FONT_SM, fill=0)

    def draw_ticker(self, label, price, change_pct, ts, invert_down=True):
        img = Image.new('1', (self.width, self.height), 255)
        d = ImageDraw.Draw(img)

        self.header(d, label)

        # Price (center)
        price_txt = f"{price:,.2f}" if isinstance(price, (int, float)) else str(price)
        pw, ph = text_wh(d, price_txt, FONT_BIG)
        d.text(((self.width - pw)//2, self.pad + 20), price_txt, font=FONT_BIG, fill=0)

        # Change (center)
        up = (isinstance(change_pct, (int,float)) and change_pct >= 0)
        arrow = "▲" if up else "▼"
        change_txt = f"{arrow} {change_pct:+.2f}%" if isinstance(change_pct, (int,float)) else str(change_pct)
        cw, ch = text_wh(d, change_txt, FONT_REG)
        d.text(((self.width - cw)//2, self.pad + 20 + ph + 8), change_txt, font=FONT_REG, fill=0)

        # Refresh policy
        if self.partial_count % 12 == 0:
            self.epd.init(self.epd.FULL_UPDATE)
        else:
            self.epd.init(self.epd.PART_UPDATE)
        self.partial_count += 1

        self.epd.display(self.epd.getbuffer(img))

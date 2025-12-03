from PIL import Image, ImageDraw, ImageFont
import math
import os

OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images')
os.makedirs(OUT_DIR, exist_ok=True)

# Demo 1: moving + pulsing circle
w,h = 480,120
frames = []
for i in range(40):
    t = i / (40-1)
    img = Image.new('RGB', (w,h), '#0f172a')
    draw = ImageDraw.Draw(img)
    x = int(40 + (440-40) * t)
    r = int(14 + 8 * (0.5 + 0.5*math.sin(t*2*math.pi*2)))
    draw.ellipse((x-r, h//2-r, x+r, h//2+r), fill='#4cc9f0')
    frames.append(img)
frames[0].save(os.path.join(OUT_DIR,'demo1.gif'), save_all=True, append_images=frames[1:], duration=60, loop=0)

# Demo 2: pulsing card
w2,h2 = 360,140
frames2 = []
for i in range(36):
    t = i / (36-1)
    img = Image.new('RGB', (w2,h2), '#001219')
    draw = ImageDraw.Draw(img)
    # pulsing brightness
    pulse = int(153 + 100 * (0.5 + 0.5*math.sin(t*2*math.pi)))
    card_color = (67,97,238, pulse)
    # draw card as rounded rect via ellipse corners
    rect_x, rect_y, rect_w, rect_h = 44,32,272,76
    draw.rounded_rectangle([rect_x, rect_y, rect_x+rect_w, rect_y+rect_h], radius=10, fill=(67,97,238))
    # overlay a semi-transparent white to simulate glow
    overlay = Image.new('RGBA', (w2,h2), (255,255,255,int(12 + 40*(0.5+0.5*math.sin(t*2*math.pi)))))
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    frames2.append(img)
frames2[0].save(os.path.join(OUT_DIR,'demo2.gif'), save_all=True, append_images=frames2[1:], duration=50, loop=0)

# Demo 3: rotating title
w3,h3 = 520,96
frames3 = []
font = None
try:
    font = ImageFont.truetype('DejaVuSans-Bold.ttf', 28)
except Exception:
    font = ImageFont.load_default()
for i in range(48):
    t = i / 48
    img = Image.new('RGBA', (w3,h3), '#0b1220')
    draw = ImageDraw.Draw(img)
    text = 'MorningMC'
    try:
        bbox = draw.textbbox((0,0), text, font=font)
        tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    except Exception:
        tw,th = font.getsize(text)
    # create text image
    txt_img = Image.new('RGBA', (tw+8, th+8), (0,0,0,0))
    txt_draw = ImageDraw.Draw(txt_img)
    txt_draw.text((4,4), text, font=font, fill='#f72585')
    angle = 360 * t
    rot = txt_img.rotate(angle, resample=Image.BICUBIC, expand=True)
    img.paste(rot, (w3//2 - rot.width//2, h3//2 - rot.height//2), rot)
    frames3.append(img.convert('RGB'))
frames3[0].save(os.path.join(OUT_DIR,'demo3.gif'), save_all=True, append_images=frames3[1:], duration=40, loop=0)

print('Generated GIFs in', OUT_DIR)

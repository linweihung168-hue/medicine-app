from PIL import Image, ImageDraw
import math

def draw_logo(size):
    img = Image.new('RGBA', (size, size), (0,0,0,0))
    d = ImageDraw.Draw(img)
    pad = int(size*0.06)
    radius = int(size*0.24)
    d.rounded_rectangle([pad, pad, size-pad, size-pad], radius=radius, fill=(251,253,255,255))

    # capsule (rotated) drawn on separate layer then pasted rotated
    cap_w, cap_h = int(size*0.62), int(size*0.21)
    cap_img = Image.new('RGBA', (cap_w, cap_h), (0,0,0,0))
    cd = ImageDraw.Draw(cap_img)
    r = cap_h//2
    cd.rounded_rectangle([0,0,cap_w,cap_h], radius=r, fill=(133,183,235,255))
    cd.rounded_rectangle([0,0,cap_w,cap_h], radius=r, fill=(133,183,235,255))
    # left dark half (rounded on left)
    left_mask = Image.new('L', (cap_w, cap_h), 0)
    lm = ImageDraw.Draw(left_mask)
    lm.rounded_rectangle([0,0,cap_w,cap_h], radius=r, fill=255)
    lm.rectangle([cap_w//2, 0, cap_w, cap_h], fill=0)
    dark = Image.new('RGBA', (cap_w, cap_h), (12,68,124,255))
    cap_img.paste(dark, (0,0), left_mask)
    # thin white divider
    cd2 = ImageDraw.Draw(cap_img)
    cd2.line([(cap_w//2,2),(cap_w//2,cap_h-2)], fill=(251,253,255,255), width=max(1,size//170))

    rotated = cap_img.rotate(35, expand=True, resample=Image.BICUBIC)
    cx, cy = int(size*0.44), int(size*0.44)
    img.alpha_composite(rotated, (cx - rotated.width//2, cy - rotated.height//2))

    # magnifier
    mag_r = int(size*0.145)
    mx, my = int(size*0.675), int(size*0.675)
    lw = max(2, size//30)
    d.ellipse([mx-mag_r, my-mag_r, mx+mag_r, my+mag_r], fill=(251,253,255,255), outline=(12,68,124,255), width=lw)
    handle_len = int(size*0.11)
    hx1 = mx + int(mag_r*0.72)
    hy1 = my + int(mag_r*0.72)
    hx2 = hx1 + int(handle_len*0.72)
    hy2 = hy1 + int(handle_len*0.72)
    d.line([(hx1,hy1),(hx2,hy2)], fill=(12,68,124,255), width=lw+1)

    return img

for s in [192, 512]:
    im = draw_logo(s)
    im.save(f'icon-{s}.png')

print("done")

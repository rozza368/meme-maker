from PIL import Image, ImageDraw, ImageFont, ImageOps
import os, time

def split_lines(text, threshold, delimiter=" "):
    """Max of `threshold` characters per line"""
    lastpos = 0
    lastspace = 0
    lines = []
    for i in range(len(text)):
        if text[i] == delimiter:
            if i - lastpos >= threshold:
                lines.append(text[lastpos:lastspace])
                lastpos = lastspace+1
            lastspace = i
    if lastpos < len(text):
        lines.append(text[lastpos:])
    return "\n".join(lines)

def save_img(img, name=None):
    if not name:
        name = int(time.time())
    img.save(f"out/{name}.png")
    print("saved image")

def trollface():
    #       w,    h
    size = (1024, 1024)
    base = Image.new("RGB", size, (255, 255, 255))
    d = ImageDraw.Draw(base)
    text_size = 84
    fnt_arial = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", size=text_size)

    imgs = ((0, "trollface"), (1, "trollge"))
    img_amt = len(imgs)
    for img in imgs:
        yval = img[0]*size[1]//img_amt
        caption = split_lines(input(f"caption for {img[0]}: "), 12)
        d.multiline_text(
            (size[0]//4, yval+size[1]//4+text_size//2), caption,
            font=fnt_arial, align="center",
            fill=(0,0,0), anchor="ms"
        )
        base.paste(
            Image.open(f"img/{img[1]}.png"),
            # halfway across image, split into top and bottom
            (size[0]//2, yval)
        )
    save_img(base)

def caption(filename, caption, text_scale=0.6, fname=None, showbase=False):
    #### around 28 characters across
    img = Image.open(f"img/{filename}")
    w, h = img.size
    # aspect > 1 if w > h (landscape), aspect < 1 if h > w (portrait)
    img_aspect = w / h
    max_aspect = 3/1
    min_aspect = 1/3
    max_size = 2160
    min_size = 256
    # how big the white caption space will be, relative to height
    caption_space = 1/5

    # ensure image is not too high or too wide
    if w < h and img_aspect < min_aspect:
        # portrait
        h = int(w*max_aspect)
        base = ImageOps.fit(img, (w, h))
    elif w > h and img_aspect > max_aspect:
        # landscape
        w = int(h*max_aspect)
        base = ImageOps.fit(img, (w, h))
    else:
        base = img

    max_dim = max(w, h)
    newsize = None
    # needs scale down
    if max_dim > max_size:
        print("scale image down")
        if w > max_size and h < max_size:
            newsize = (max_size, max_size/img_aspect)
        elif h > max_size and w < max_size:
            newsize = (max_size*img_aspect, max_size)
        else:
            if w < h:
                newsize = (max_size*img_aspect, max_size)
            elif w > h:
                newsize = (max_size, max_size/img_aspect)
            else:
                newsize = (min_size, min_size)
    # needs scale up
    elif max_dim < min_size:
        print("scale image up")
        if w < min_size and h > min_size:
            newsize = (min_size, min_size/img_aspect)
        elif w > min_size and h < min_size:
            newsize = (min_size*img_aspect, min_size)
        else:
            if w < h:
                newsize = (min_size*img_aspect, min_size)
            elif w > h:
                newsize = (min_size, min_size/img_aspect)
            else:
                newsize = (min_size, min_size)

    if newsize:
        base = base.resize((int(newsize[0]), int(newsize[1])))

    if showbase: base.show()

    w, h = base.size
    padding_scale = (1 - text_scale) / 2
    caption_height = int(caption_space*h)
    # 1080 pixels across, approx 13 characters, 0.65 aspect ratio
    ### TODO add text resizing
    textmod = 1
    if img_aspect > 1:
        textmod = img_aspect
        print("applied text mod")
    text_size = int(caption_height*text_scale*textmod)
    fnt = ImageFont.truetype("font/impact.ttf", size=text_size)

    white = Image.new("RGB", (w, h+caption_height), (255,255,255))
    # paste image at bottom of white
    white.paste(base, (0, caption_height))
    d = ImageDraw.Draw(white)
    d.text(
        # halfway across, compensate for font size with small amount
        (w//2, int(caption_height * (1 - padding_scale - 0.08))),
        caption, font=fnt, anchor="ms", fill=(0,0,0)
    )
    save_img(white, fname)

caption("trollface.png", "test")
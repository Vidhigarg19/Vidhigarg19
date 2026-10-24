from PIL import Image, ImageDraw

SIZE, RING = 600, 10
im = Image.open("assets/avatar-raw.png").convert("RGBA")
w, h = im.size
s = min(w, h)
im = im.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2)).resize((SIZE, SIZE))

ring = Image.new("RGBA", (SIZE, SIZE))
px = ring.load()
for x in range(SIZE):
    for y in range(SIZE):
        t = (x + y) / (2 * SIZE)
        px[x, y] = (int(168 + (34 - 168) * t), int(85 + (211 - 85) * t), int(247 + (238 - 247) * t), 255)

mask_out = Image.new("L", (SIZE, SIZE), 0)
ImageDraw.Draw(mask_out).ellipse((0, 0, SIZE - 1, SIZE - 1), fill=255)
mask_in = Image.new("L", (SIZE, SIZE), 0)
ImageDraw.Draw(mask_in).ellipse((RING, RING, SIZE - 1 - RING, SIZE - 1 - RING), fill=255)

out = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
out.paste(ring, (0, 0), mask_out)
out.paste(im, (0, 0), mask_in)
out.save("assets/avatar.png")
print("avatar saved")
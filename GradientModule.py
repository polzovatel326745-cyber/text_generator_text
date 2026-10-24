from PIL import Image,ImageDraw,ImageFont,ImageFilter,features
from math import ceil,floor
import os, keyboard, pyperclip, time, requests, json

"""
from fontTools import ttLib, merge
def make_font(font_list, output_to):
    merger = merge.Merger()
    font = merger.merge(font_list)
    #metrics = read_line_metrics(ttLib.TTFont(font_list[0]))
    #set_line_metrics(font, metrics)
    font.save(output_to)
    font.close()

make_font(["TextMaker/Fonts/discord.ttf","NotoSans.ttf","HelveticaNeue.ttf"],"DiscordFont")
#make_font(["Helvetica.ttf","Arial.ttf"],"Helvetica_Arial.ttf")
#make_font(["Helvetica_Arial.otf","Discord_NotoSans.ttf"],"DiscordFontAAA")
"""

def create_gradient(size, start_color, end_color, direction='vertical'):
    gradient = Image.new('RGBA', size)
    draw = ImageDraw.Draw(gradient)

    if direction == 'vertical':
        for y in range(size[1]):
            r = int(start_color[0] * (1 - y / size[1]) + end_color[0] * (y / size[1]))
            g = int(start_color[1] * (1 - y / size[1]) + end_color[1] * (y / size[1]))
            b = int(start_color[2] * (1 - y / size[1]) + end_color[2] * (y / size[1]))
            a = int(start_color[3] * (1 - y / size[1]) + end_color[3] * (y / size[1]))
            draw.line([(0, y), (size[0], y)], fill=(r, g, b, a))
    elif direction == 'horizontal':
        for x in range(size[0]):
            r = int(start_color[0] * (1 - x / size[0]) + end_color[0] * (x / size[0]))
            g = int(start_color[1] * (1 - x / size[0]) + end_color[1] * (x / size[0]))
            b = int(start_color[2] * (1 - x / size[0]) + end_color[2] * (x / size[0]))
            a = int(start_color[3] * (1 - x / size[0]) + end_color[3] * (x / size[0]))
            draw.line([(x, 0), (x,size[1])], fill=(r, g, b, a))
    return gradient

def hextorgba(h):
    h = h.lstrip("#")
    r,g,b = h[0:2],h[2:4],h[4:6]
    print(r,g,b)
    return (int(r,base=16),int(g,base=16),int(b,base=16),255)

class TextGradient:
    def generategradienttext(text,colors,size:int=1):
        try:
            font = ImageFont.truetype("DiscordFontNew.ttf",18*size)
        except:
            font = ImageFont.truetype("DiscordFontNew.ttf",18*size)

        frames = []
        width = ceil(font.getlength(text))+8+15
        height = ((font.size+5)*(text.count("\n")+1))-3+1*size
        gradientwidth = 100*size
        for i in range(gradientwidth):
            if i%8!=0:
                continue
            img = Image.new("RGBA",(width,height),(0,0,0,0))#(ceil(font.getlength(text))+2, font.size-2)

            draw = ImageDraw.ImageDraw(img)
            
            newimg = img.copy()
            newdraw = ImageDraw.ImageDraw(newimg)
            newdraw.text((3*size+5,-3),text,(0,0,0,170),font)
            imfilter = ImageFilter.GaussianBlur(2.5*size)
            newimg = newimg.filter(imfilter)
            img.paste(newimg)

            draw.text((3*size+5,-3),text,(0,0,0),font)

            gradient = Image.new("RGBA",(ceil(width/gradientwidth)*gradientwidth,height))

            gradient1 = create_gradient((ceil(gradientwidth/2),height),colors[0],colors[1],'horizontal')
            gradient2 = create_gradient((ceil(gradientwidth/2),height),colors[1],colors[0],'horizontal')

            gradient.paste(gradient1)
            gradient.paste(gradient2,(ceil(gradientwidth/2),0))

            for x in range(ceil(width/gradientwidth)):
                gradient.paste(gradient,(x*gradientwidth,0))

            #gradient = gradient.resize(img.size)
            gradient = roll(gradient,-i)

            r,g,b,a = img.split()
            gr,gg,gb,ga = gradient.split()

            r.paste(gr)
            g.paste(gg)
            b.paste(gb)
            #a = a.point(lambda i: round(i/255)*255)

            newimg = Image.merge("RGBA",(r,g,b,a))
            frames.append(newimg)

        if len(frames)<=0:
            return

        frames[0].save(
            "gradientanim.webp",
            save_all=True,
            append_images=frames[1:],
            duration=1,
            loop=0,
            optimize=False,
            disposal=2,
            palettesize=256,
            comment="generated_gradient_"+text
        )

        return frames

def roll(im: Image.Image, delta: int) -> Image.Image:
    """Roll an image sideways."""
    xsize, ysize = im.size

    delta = delta % xsize
    if delta == 0:
        return im

    part1 = im.crop((0, 0, delta, ysize))
    part2 = im.crop((delta, 0, xsize, ysize))
    im.paste(part1, (xsize - delta, 0, xsize, ysize))
    im.paste(part2, (0, 0, xsize - delta, ysize))

    return im

"""frames:list[Image.Image] = TextGradient.generategradienttext("text",((230, 30, 139, 255),(240, 112, 157, 255)),4)
cellsize = frames[0].height
nframes = []

for _ in range(ceil(frames[0].width/cellsize)*ceil(frames[0].height/cellsize)):
    nframes.append([])
i = 0

print("Creating...")
for frame in frames:
    n = Image.new("RGBA",(ceil(frame.width/cellsize)*cellsize,ceil(frame.height/cellsize)*cellsize))
    n.paste(frame)

    j = 0
    for x in range(ceil(n.width/cellsize)):
        for y in range(ceil(n.height/cellsize)):
            cropped = n.crop((x*cellsize,y*cellsize,x*cellsize+cellsize,y*cellsize+cellsize))
            nframes[j].append(cropped)
            j += 1
    i += 1
    print(i)

print("Saving...")

try:
    dir = os.makedirs("output")
except:
    print("already")

i = 0
for gif in nframes:
    gif[0].save(
            "output/"+str(i)+"_frame.webp",
            save_all=True,
            append_images=gif[1:],
            duration=1,
            loop=0,
            optimize=False,
            disposal=2,
            palettesize=256
        )
    i += 1
    print(i)
print("Done!")"""
from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
from GradientModule import TextGradient
import io

app = Flask(__name__)

def rgb(h):
    h = h.lstrip("#")
    return (int(h[0:2],16),int(h[2:4],16),int(h[4:6],16))

@app.route("/text")
def img():
    text = request.args.get("t", "use param 't' to change text")
    clr1 = request.args.get("color1", "7e1faa")
    clr2 = request.args.get("color2", "1f5baa")

    print(clr1,clr2)
    frames = TextGradient.generategradienttext(text,(rgb(clr1)+(255,0),rgb(clr2)+(255,0)))
    
    buf = io.BytesIO()
    frames[0].save(buf,
            save_all=True,
            format="WEBP",
            append_images=frames[1:],
            duration=1,
            loop=0,
            optimize=False,
            disposal=2,
            palettesize=256,
            comment="generated_gradient_"+text)
    buf.seek(0)
    return send_file(buf, mimetype="image/webp")

if __name__ == "__main__":
    app.run(port=5000)
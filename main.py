import click
from PIL import Image
import requests
from io import BytesIO
import tqdm


DEFAULT_URL = "http://stamen-tiles-a.a.ssl.fastly.net/watercolor"
# NYC: (9642, 12319)
# Cambridge: (9905, 12110)
# Princeton: (9583, 12355)

@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("--url", "-u", type=str, default=DEFAULT_URL, help="Base URL")
@click.option("-x", type=int, default=9642, help="x coordinate")
@click.option("-y", type=int, default=12310, help="y coordinate")
@click.option("-z", type=int, default=15, help="z coordinate")
@click.option("-w", type=int, default=12, help="Width in tiles")
@click.option("-h", type=int, default=18, help="Height in tiles")
@click.option("-o", type=click.Path(), default="map.jpg", help="Output file path")
@click.option("-d", type=int, default=256, help="Tile width or height in pixels")
def main(url, x, y, z, w, h, o, d):
    print(locals())

    result = Image.new("RGB", (w * d, h * d))
    for i in tqdm.tqdm(range(w), leave=True):
        for j in tqdm.tqdm(range(h), leave=False):
            response = requests.get(f'{url}/{z}/{x + i}/{y + j}.jpg')
            img = Image.open(BytesIO(response.content))
            result.paste(im=img, box=(i * d, j * d))

    result.save(o)


if __name__ == "__main__":
    main()

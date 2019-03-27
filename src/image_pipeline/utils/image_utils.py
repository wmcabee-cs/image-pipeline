import matplotlib.pyplot as plt
import matplotlib.patches as patches
from itertools import zip_longest, starmap
import requests
import numpy as np
from PIL import Image
import io

from image_pipeline.utils.pipeline_utils import map_merge


def vertices2patch(vertices):
    ''' Converts bounding box format returned from google into bounding box format required by matplot lib'''
    values = [(x['x'], x['y']) for x in vertices]
    x_values, y_values = zip(*values)
    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)
    return {'xy': (x_min, y_min),
            'width': x_max - x_min,
            'height': y_max - y_min}


def _prep_for_matplotlib(image):
    # Add image and image shape to object
    print(f">> fetching image {image['image_url']}")
    r = requests.get(image['image_url'])
    r.raise_for_status()
    im = np.array(Image.open(io.BytesIO(r.content)), dtype=np.uint8)

    # convert bounding box into format required by matplotlib
    bounding_box = vertices2patch(image['bounding_box'])
    output = {'im': im, 'bounding_box': bounding_box}
    return output


def _show_image(ax, image):
    if image is None:
        ax.set_visible(False)
        return
    ax.imshow(image['im'])

    # add bounding box rectangle
    rect = patches.Rectangle(linewidth=2, edgecolor='r', facecolor='none', **image['bounding_box'])
    ax.add_patch(rect)


DEFAULT_FIGURE_SIZE = [12, 12]


def show_images(image_list, columns=3, figsize=DEFAULT_FIGURE_SIZE):
    # prepare display dataset
    reader = map(_prep_for_matplotlib, image_list)
    images = list(reader)

    # Create a grid of matplotlib axes
    rows = (len(images) // columns) + 1
    fig, axes = plt.subplots(rows, columns, figsize=figsize)
    axes = axes.ravel()

    # Render the images into the axes
    reader = images
    reader = zip_longest(axes, reader)
    reader = starmap(_show_image, reader)
    for _ in reader:
        pass

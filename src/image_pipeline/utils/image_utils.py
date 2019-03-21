import matplotlib.pyplot as plt
import matplotlib.patches as patches
from itertools import zip_longest
import requests
import numpy as np
from PIL import Image
import io


def _show_image(ax, image):
    if image is None:
        ax.set_visible(False)
        return
    ax.imshow(image['_im'])

    # add bounding box rectange
    rect = patches.Rectangle(linewidth=2, edgecolor='r', facecolor='none', **image['_bounding_box'])
    ax.add_patch(rect)


def vertices2patch(vertices):
    ''' Converts bounding box format returned from google into bounding box format required by matplot lib'''
    values = [(x['x'], x['y']) for x in vertices]
    x_values, y_values = zip(*values)
    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)
    return {'xy': (x_min, y_min),
            'width': x_max - x_min,
            'height': y_max - y_min}


def prep_for_matplotlib(image):
    # Add image and image shape to object
    print(f">> fetching image {image['image_url']}")
    r = requests.get(image['image_url'])
    r.raise_for_status()
    im = np.array(Image.open(io.BytesIO(r.content)), dtype=np.uint8)
    image['_im'] = im
    image['_shape'] = im.shape

    # convert bounding box into format required by matplotlib
    bounding_box = vertices2patch(image['boundingPoly'])
    image['_bounding_box'] = bounding_box
    return image


def show_images(image_list, columns=3, figsize=[12, 12]):
    image_list = list(map(prep_for_matplotlib, image_list))
    rows = (len(image_list) // columns) + 1

    fig, axes = plt.subplots(rows, columns, figsize=figsize)
    axes = axes.ravel()
    reader = zip_longest(axes, image_list)
    for ax, image in reader:
        _show_image(ax=ax, image=image)

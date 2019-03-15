import numpy as np


def ident_colors(image_url):
    def mock_color():
        return dict(fractionOfPixels=np.round(np.random.random(), 2),
                    rgbValues='rgb_str',
                    score=np.random.randint(1, 10 + 1), )

    return [mock_color() for x in range(np.random.randint(0, 5))]


def ident_bounding_boxes(image_url):
    def mock_box():
        return dict(boundingPoly=list(np.random.randint(1, 100 + 1, size=4)),
                    confidence=np.round(np.random.random(), 2),
                    importanceFraction=np.round(np.random.random(), 2), )

    return [mock_box() for x in range(np.random.randint(0, 5))]


def ident_landmarks(image_url):
    def mock_landmarks():
        return dict(landmark='identified landmark', confidence=np.round(np.random.random(), 2))

    return [mock_landmarks() for x in range(np.random.randint(1, 2))]

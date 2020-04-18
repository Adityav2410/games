import cv2
import numpy as np

GRAYSCALE_VALUE = 211

def clip(x, minval, maxval):
    if x <= minval:
        return minval
    if x >= maxval:
        return maxval
    return x

def display_blocks_and_get_user_input(arena, blocks, title):
    w, h = arena.width, arena.height
    image = np.ones((h, w, 3), dtype=np.uint8) * GRAYSCALE_VALUE
    
    for block in blocks:
        bbox = block.bbox
        for k, v in bbox.items():
            bbox[k] = int(v)
        p1 = (clip(bbox["tlx"], 0, w), clip(bbox["tly"], 0, h))
        p2 = (clip(bbox["brx"], 0, w), clip(bbox["bry"], 0, h))

        if block.meta is not None and isinstance(block.meta, dict) and "color" in block.meta:
            color = block.meta["color"]
        else:
            color = (0, 0, 0)
        
        image = cv2.rectangle(image, p1, p2, color, -1)
    cv2.imshow(title, image)
    user_input = cv2.waitKey(33)
    return user_input
        
        
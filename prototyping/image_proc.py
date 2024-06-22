'''
Series of functions for processing an image to make it easier identifiable
by pytesseract.

Functions include:
'''

from typing import List
# TODO Implement multiprocessing for better conversion to 3-dim list
# from multiprocessing.dummy import Pool
import numpy as np
from PIL import Image

# Convert the image to array of pixels
def to_array(img: Image) -> List:
    # Use numpy to convert image to array of pixels
    ar = np.array(img)
    # This conversion creates a significant amount of extra metadata.
    # This metadata isn't needed for this use, and adds processing time,
    # so we'll instead convert this numpy.ndarray into specifically
    # a 3-dimensional list and return that.
    return ar_to_list(ar)

# Convert an numpy.ndarray to a 3-dimensional list
def ar_to_list(ar: np.ndarray) -> List:
    # Return list
    ar_list = []
    # Check dimension of self
    if ar.ndim == 1:
        # If only one dimensional, convert directly to list
        for el_index in range(ar.size):
            ar_list.append(int(ar[el_index]))
    # If not,
    else:
    # recursively get each element as a list instead of an ndarray
        for el in ar:
            ar_list.append(ar_to_list(el))
    # Return the constructed list
    return ar_list

# Find the nth most common color in an image
def nth_common_color(pixel_ar: List, n: int) -> List[int]:
    # Note that the first number in the address is y coord,
    # second number in the address is x coord.
    y_size = len(pixel_ar)
    x_size = len(pixel_ar[0])
    # List of colors and their frequencies
    color_list = []
    freq_list = []
    # Identify each pixel's color and track frequencies
    for y in range(y_size):
        for x in range(x_size):
            # Check if color has been seen before
            try:
                # If an index is returned, it has been seen before
                index = color_list.index(pixel_ar[y][x])
                # Increment the associated spot in the frequency list
                freq_list[index] += 1
            except ValueError:
                # If a ValueError is raised, it has not been seen before
                # Add it to the color list
                color_list.append(pixel_ar[y][x])
                # Append a 1 to frequency list since the color has now been
                # seen once and the indexes of both color and freq will match.
                freq_list.append(1)
    # Once pixel colors have been counted, combine the two lists and sort
    # by frequency
    full_list = []
    for color in enumerate(color_list):
        full_list.append((color[1], freq_list[color[0]]))
    full_list.sort(key=freq_of_color, reverse=True)
    return full_list[n][0]

# Get frequency from color/frequency tuple
def freq_of_color(tup: tuple[List, int]) -> int:
    return tup[1]

# Replace the nth most common color with a specified color
def keep_nth_color(pixel_ar: List, n: int, color: List) -> None:
    # Get the most common pixel color
    nth_color = nth_common_color(pixel_ar, n)
    # Replace every instance of that color with the specified color
    for y_line in enumerate(pixel_ar):
        for x_dot in enumerate(y_line[1]):
            if x_dot[1] != nth_color:
                pixel_ar[y_line[0]][x_dot[0]] = color
    # Colors have been modified, return None
    return

# Replace anything not close to black with white
def remove_all_color(pixel_ar: List) -> None:
    # Note that the first number in the address is y coord,
    # second number in the address is x coord.
    y_size = len(pixel_ar)
    x_size = len(pixel_ar[0])
    # Identify each pixel's color and track frequencies
    for y in range(y_size):
        for x in range(x_size):
            # Check if color is close to black by seeing if any colors
            # are more present than others
            color = pixel_ar[y][x]
            if (color[0] != color[1] or
                color[0] != color[2] or
                color[1] != color[2]):
                pixel_ar[y][x] = [255, 255, 255, 255]
    # Done, return None
    return

img_ar = to_array(Image.open('prototyping/prompt.png'))
remove_all_color(img_ar)
img = Image.fromarray(np.array(img_ar, dtype=np.uint8), mode='RGBA')
img.save("prototyping/prompt.png")

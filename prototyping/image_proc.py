'''
Series of functions for processing an image to make it easier identifiable
by pytesseract.

Functions include:
'''

from math import sqrt
from typing import List
# TODO Implement multiprocessing for better conversion to 3-dim list
# from multiprocessing.dummy import Pool
import numpy as np
from PIL import Image

# Class to hold image as an array with variables to be set during creation
# to prevent recalculation regularly
class img_as_array:

    # Class specific variabls to simplify recursion
    color_list = []
    freq_list = []

    def __init__(self, im: Image):
        # Use numpy to convert image to array of pixels
        ar = np.array(im)
        # This conversion creates a significant amount of extra metadata.
        # This metadata isn't needed for this use, and adds processing time,
        # so we'll instead convert this numpy.ndarray into specifically
        # a 3-dimensional list and return that.
        self.pixel_ar = self.ar_to_list(ar)
        # Once pixel colors have been counted, combine the two lists and sort
        # by frequency
        full_list = []
        for color in enumerate(self.color_list):
            # Combine two lists
            full_list.append((color[1], self.freq_list[color[0]]))
        # Sort descending based on the frequency half of the tuple
        full_list.sort(key=self.freq_of_color, reverse=True)
        self.color_freq_list = full_list
        # Set width and height of the image
        self.height = len(self.pixel_ar)
        self.width = len(self.pixel_ar[0])

    # Convert an numpy.ndarray to a 3-dimensional list
    def ar_to_list(self, ar: np.ndarray) -> List:
        # Return list
        ar_list = []
        # Check dimension of self
        if ar.ndim == 1:
            # If only one dimensional, just a pixel: convert directly to list
            for el_index in range(ar.size):
                ar_list.append(int(ar[el_index]))
            # Then check frequency for that pixel's color
            try:
                # If an index is returned, it has been seen before
                index = self.color_list.index(ar_list)
                # Increment the associated spot in the frequency list
                self.freq_list[index] += 1
            except ValueError:
                # If a ValueError is raised, it has not been seen before
                # Add it to the color list
                self.color_list.append(ar_list)
                # Append a 1 to frequency list since the color has now been
                # seen once and the indexes of both color and freq will match.
                self.freq_list.append(1)
        # If not,
        else:
        # recursively get each element as a list instead of an ndarray
            for el in ar:
                ar_list.append(self.ar_to_list(el))
        # Return the constructed list
        return ar_list

    # Get frequency from color/frequency tuple
    def freq_of_color(self, tup: tuple[List, int]) -> int:
        return tup[1]

# Find the nth most common color in an image
def nth_common_color(ar_img: img_as_array, n: int) -> List[int]:
    # Get the nth most common color from the color_freq_list variable
    return ar_img.color_freq_list[n][0]

# Replace the nth most common color with a specified color
def keep_nth_color(ar_img: img_as_array, n: int, color: List) -> None:
    # Get the most common pixel color
    nth_color = nth_common_color(ar_img, n)
    # Replace every instance of that color with the specified color
    for y_line in enumerate(ar_img.pixel_ar):
        for x_dot in enumerate(y_line[1]):
            if x_dot[1] != nth_color:
                ar_img.pixel_ar[y_line[0]][x_dot[0]] = color
    # Colors have been modified, return None
    return

# Replace anything not close to black with white
def remove_all_color(ar_img: img_as_array) -> None:
    # Note that the first number in the address is y coord,
    # second number in the address is x coord.
    for y in range(ar_img.height):
        for x in range(ar_img.width):
            # Check if color is close to black by seeing if any colors
            # are more present than others
            color = ar_img.pixel_ar[y][x]
            if not (color[0] == color[1] and
                    color[1] == color[2]):
                ar_img.pixel_ar[y][x] = [255, 255, 255, 255]
    # Done, return None
    return

# Virtualizes color as 3 dimensional space with each RGB as an axis
# and returns the distance between two colors in that space
def dist_between_colors(color_one: List, color_two: List) -> float:
    # If each color is an axis in 3 dimensions then distance is simple
    # d = sqrt((x2-x1)^2+(y2-y1)^2+(z2-z1)^2). This ignores alpha value
    # Take each number as a float explicitly to give accurate results
    r_sq = (float(color_two[0]) - float(color_one[0])) ** 2
    g_sq = (float(color_two[1]) - float(color_one[1])) ** 2
    b_sq = (float(color_two[2]) - float(color_one[2])) ** 2
    dist = sqrt(sum([r_sq, g_sq, b_sq]))
    return dist

# Normalize an image by identifying the text color, then removing everything
# except colors within an acceptable range of that color
def proccess_image(ar_img: img_as_array) -> None:
    # Find most common color (background)
    bg_color = nth_common_color(ar_img, 0)
    # Iterate through remaining colors until one distinct enough to be
    # text is found
    text_color = []
    for i in range(1, len(ar_img.color_freq_list) - 1):
        cur_color = nth_common_color(ar_img, i)
        if dist_between_colors(bg_color, cur_color) > 50:
            text_color = cur_color
            break
    # Iterate through all pixels
    for y in range(ar_img.height):
        for x in range(ar_img.width):
            # Check if color is close enough, if not remove
            color = ar_img.pixel_ar[y][x]
            if dist_between_colors(color, text_color) > 125:
                ar_img.pixel_ar[y][x] = bg_color
            # If it is, replace it with the text color
            else:
                ar_img.pixel_ar[y][x] = text_color
    # Done, return None
    return



img_ar_obj = img_as_array(Image.open('prototyping/prompt.png'))
proccess_image(img_ar_obj)
img = Image.fromarray(np.array(img_ar_obj.pixel_ar, dtype=np.uint8), mode='RGBA')
img.save("prototyping/prompt.png")

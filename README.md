jellybean
=========

CS 231A Project

OpenCV
------

To install OpenCV for Python, install homebrew (if you haven't already) and run `brew install opencv`. You will also need numpy (a package that gives Python matlab-like capabilities) which you can install with `pip install numpy`.

Watershed
---------

Finally got some shitty version of watershed working. See `watershed.py` and `img/wshed.jpg`. When you write it up go through the algorithm, which I outline in the comments. (If I have time I can do that.)

Now all that's left is to figure out how to determine the number based on the location and area of the top right and bottom left jellybean, then extrapolating. It's definitely a gross approximation.

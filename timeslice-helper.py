import glob
import os
import sys

from PIL import Image


# Open an Image
def open_image(path):
    newImage = Image.open(path)
    return newImage


# Save Image
def save_image(image, path):
    image.save(path, 'png')


# Create a new image with the given size
def create_image(i, j):
    image = Image.new("RGB", (i, j), "white")
    return image


# Get the pixel from the given image
def get_pixel(image, i, j):
    # Inside image bounds?
    width, height = image.size
    if i > width or j > height:
        return None

    # Get Pixel
    pixel = image.getpixel((i, j))
    assert isinstance(pixel, object)
    return pixel


def slice(images):
    # Get size
    width, height = images[0].size

    # calculate slices
    s = round(width / len(images))
    print("Each slice will be " + str(s) + "pixel wide.")
    slices = []
    for x in images:
        slices.append(s)
    if (s * len(images)) < width:
        slices[len(images) - 1] = slices[len(images) - 1] + (width - (s * len(images)))
        print("The last slice will be " + str(width - (s * len(images))) + "pixel bigger.")

    # Create new Image and a Pixel Map
    new = create_image(width, height)
    pixels = new.load()

    current = 0
    # column
    c = 0
    for row in slices:
        print("Slicing image " + str(c + 1))
        for i in range(current, current + row):
            for j in range(height):
                # Set Pixel in new image
                pixels[i, j] = get_pixel(images[c], i, j)
        c = c + 1
        current = current + row
    # Return new image
    return new


def check_files(images):
    width, height = images[0].size
    if len(images) > width:
        print("To many images. Each slice would be smaller than 1px.")
        return
    print("The output image will be " + str(width) + "x" + str(height))
    for x in images:
        w, h = x.size
        if w != width or h != height:
            return False
    return True


def get_dir(path):
    dir = []
    for currentpath, folders, files in os.walk(path):
        for folder in folders:
            print(os.path.join(currentpath, folder))
            dir.append(os.path.join(currentpath, folder))

    for d in dir:
        print("Processing " + str(d))
        process_dir(d, "")


def process_dir(d, name):
    files = []
    images = []

    # Load Image (JPEG/JPG needs libjpeg to load)
    for file_name in sorted(glob.iglob(d + '/*.jpg', recursive=True)):
        files.append(file_name)
        images.append(open_image(file_name))
    # check if folder contains no images
    if not files:
        print("This folder contains no images.")
        return

    if check_files(images):
        print("All images have the same size.")
    else:
        print("Not all images have the same size.")
        return

    print("Processing " + str(len(images)) + " images.")

    # Slice and save
    new = slice(images)
    print("Saving image...")
    filename = ""
    if name == "":
        filename = str(d).replace("/", '_')
    else:
        filename = name.replace("/", '_')
    p = "output/" + filename.replace("\\", '_')
    save_image(new, p + '.jpg')
    print(p + ".jpg is ready.")


# Main
if __name__ == "__main__":

    path = sys.argv[1]
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        sys.exit("Path is not a directory or does not exist.")
    rec = sys.argv[2]
    name = ""
    #
    if len(sys.argv) > 3:
        name = sys.argv[3]
    if rec == "True":
        get_dir(path)
    else:
        process_dir(path, name)

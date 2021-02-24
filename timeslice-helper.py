import glob
import os
import sys

from PIL import Image


# Open an Image
def open_image(path) -> object:
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


def slice(files):
    # Get size
    width, height = open_image(files[0]).size

    # calculate slices
    s = int((width / len(files)))
    print("Each slice will be " + str(s) + "pixel wide.")
    slices = []
    for x in files:
        slices.append(s)
    if (s * len(files)) < width:
        print("Distributing lextover columns.")
        leftover = width - (s * len(files))
        print(str(leftover))
        for i in range((len(files) - 1), 0, -1):
            if leftover > 0:
                slices[i] = slices[i] + 1
                leftover = leftover - 1
                print("Image " + str(i) + " will be 1px bigger.")
        # slices[len(files) - 1] = slices[len(files) - 1] + (width - (s * len(files)))
        print("Leftover pixel-columns were distributed evenly among the leftmost slices.")

    # Create new Image and a Pixel Map
    new = create_image(width, height)
    pixels = new.load()

    current = 0
    # column
    c = 0
    for row in slices:
        pic = open_image(files[c])
        print("Slicing image " + str(c + 1) + " - " + str(slices[c]) + " Pixels wide.")
        for i in range(current, current + row):
            for j in range(height):
                # print(str(c+1) + " - " + str(i) + " - " + str(j))
                # Set Pixel in new image
                pixels[i, j] = get_pixel(pic, i, j)
        c = c + 1
        current = current + row
    # Return new image
    return new


def check_files(files):
    width, height = open_image(files[0]).size
    if len(files) > width:
        print("To many images. Each slice would be smaller than 1px.")
        return
    print("The output image will be " + str(width) + "x" + str(height))
    for x in files:
        w, h = open_image(x).size
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
    # check if folder contains no images
    if not files:
        print("This folder contains no images.")
        return

    if check_files(files):
        print("All images have the same size.")
    else:
        print("Not all images have the same size.")
        return

    print("Processing " + str(len(files)) + " images.")

    # Slice and save
    new = slice(files)
    print("Saving image...")
    filename = ""
    if name == "":
        filename = str(d).replace("/", '_')
    else:
        filename = name.replace("/", '_')
    p = "output/" + filename.replace("\\", '_')
    save_image(new, p + '.png')
    print(p + ".png is ready.")


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

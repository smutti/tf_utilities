#!/usr/bin/env python

from PIL import Image
import os
import argparse

def rescale_images(directory):
    """ This function autorotates a picture """
    
    print("Start Processing...")
    for img in os.listdir(directory):
        print("Processing ", img)
        image = Image.open(os.path.join(directory, img))
        try:
                exif = image._getexif()
        except AttributeError as e:
            print("Could not get exif - Bad image!")
            return

        (width, height) = image.size
        # print "\n===Width x Heigh: %s x %s" % (width, height)
        if not exif:
                if width > height:
                    image = image.rotate(90)
                    image.save(os.path.join(directory, img), quality=100)
                    continue
        else:
                orientation_key = 274 # cf ExifTags
                if orientation_key in exif:
                    orientation = exif[orientation_key]
                    rotate_values = {
                            3: 180,
                            6: 270,
                            8: 90
                    }
                    if orientation in rotate_values:
                            # Rotate and save the picture
                            image = image.rotate(rotate_values[orientation])
                            image.save(os.path.join(directory, img), quality=100, exif=str(exif))
                            continue
                else:
                    if width > height:
                        image = image.rotate(90)
                        image.save(os.path.join(directory, img), quality=100, exif=str(exif))
                        continue
    
    print("Stop Processing")
        #im_rotated = im.transpose(Image.ROTATE_180)
        #im_rotated.save(os.path.join(directory, img))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Rescale images")
    parser.add_argument('-d', '--directory', type=str, required=True, help='Directory containing the images')
    args = parser.parse_args()
    rescale_images(args.directory)
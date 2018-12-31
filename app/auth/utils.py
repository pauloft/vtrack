import os
import secrets
from PIL import Image
from PIL.ExifTags import TAGS
from flask import url_for, current_app
from flask_mail import Message
from app import mail

# processing specifically for profile images
def save_picture(form_picture, folder="static/profile_thumbs"):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.split(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, folder, picture_fn)
    # resize the image and save
    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Password Reset Request", sender="noreply@demo.com", recipients=[user.email]
    )
    msg.body = f"""To reset your password, visit the following link:
{url_for('auth.reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
"""
    mail.send(msg)


""" 
Processing for pictures
"""


def mkdir(dirname):
    """ Make a folder at dirname """
    try:
        os.mkdir(dirname)
    except Exception:
        pass


def maxSize(image, maxSize, method=3):
    """ Determine the max size of the image """
    imAspect = float(image.size[0]) / float(image.size[1])
    outAspect = float(maxSize[0] / float(maxSize[1]))

    if imAspect >= outAspect:
        return image.resize(
            (maxSize[0], int((float(maxSize[0]) / imAspect) + 0.5)), method
        )
    else:
        return image.resize(
            (int((float(maxSize[1]) * imAspect) + 0.5), maxSize[1]), method
        )


def processImage(picture_data, target_dir):
    """ Process the picture image, save it and a thumbnail in respective folders
    -- given a new filename (random hex char string)
    -- picture_data is the form.<fieldname>.data from the POST operation
    """
    img = Image.open(picture_data)
    exif = img._getexif()
    if exif is not None:
        for tag, value in exif.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "Orientation":
                if value == 3:
                    img = img.rotate(180)
                if value == 6:
                    img.rotate(270)
                if value == 8:
                    img.rotate(90)
                break
    img = maxSize(img, (1024, 768), Image.ANTIALIAS)
    # generate a random 8-byte (i.e. 16-character string)
    random_hex = secrets.token_hex(8)
    # split the filename to get the extension
    _, f_ext = os.path.split(picture_data.filename)
    # generate the new filename
    new_filename = random_hex + f_ext
    # calculate the full path to save the file, and save it
    path_to_save = os.path.join(current_app.root_path, target_dir, new_filename)
    # thumbs directory
    thumbs_dir = os.path.join(current_app.root_path, target_dir, "thumbs")
    if not os.path.exists(thumbs_dir):
        os.mkdir(thumbs_dir)
    img.save(path_to_save, "JPEG", quality=100)
    img.thumbnail((300, 300))
    img.save(os.path.join(thumbs_dir, new_filename))

    return new_filename

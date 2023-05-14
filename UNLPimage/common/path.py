import os

# constants  paths
PATH = os.path.abspath(os.path.realpath("."))


def path(*args):
    return os.path.join(PATH, "UNLPimage", *args)


PATH_SETTINGS_ICO = path("static", "icon", "-settings-big-.png")
PATH_PLUS_ICO = path("static", "icon", "-plus-icon-.png")
PATH_HELP_ICO = path("static", "icon", "-help-ldark-big-.png")
PATH_BACK_ICO = path("static", "icon", "-back-big-.png")
PATH_PFP_ICO = path("static", "icon", "-pfp-big-.png")
PATH_IMAGE_AVATAR = path("images", "avatar")
PATH_DATA_JSON = path("data", "json_files")
PATH_DATA_CSV = path("data", "csv_files")
PATH_DEFAULT_IMAGES = path("images", "images")
PATH_DEFAULT_MEMES = path("images", "meme")
PATH_DEFAULT_COLLAGE = path("images", "collage")
PATH_JSON = path("data", "json_files", "directories.json")
PATH_CSV = path("data", "csv_files")
PATH_FONT = path("static", "font", "Roboto-Black.ttf")

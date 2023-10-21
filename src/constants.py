from enum import Enum

BUCKET_NAME = "sandbox-98197.appspot.com"

class Collection(str, Enum):
    Sprite = "sprite"
    Comics = "comics"
    User = "user"
    Preview = "preview"

class SpriteCategory(str, Enum):
    Character = "character"
    Background = "background"
    
from slugify import slugify

def generate_slug(name: str) -> str:
    return slugify(name)
from sqlmodel import Session, select

from slugify import slugify

def generate_slug(db: Session, model, base_value: str, slug_field: str = "slug") -> str:
    base_slug = slugify(base_value)
    slug = base_slug
    index = 1

    while db.exec(select(model).where(getattr(model, slug_field) == slug)).first():
        slug = f"{base_slug}-{index}"
        index += 1

    return slug

def update_model_instance(data: dict, item):
    for key, value in data.items():
        setattr(item, key, value)
    return item

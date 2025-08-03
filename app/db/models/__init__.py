from .product import *
from .user import *
from .base import *

Product.model_rebuild()
Category.model_rebuild()
CategoryProductPivot.model_rebuild()
User.model_rebuild()
RolePermissionLink.model_rebuild()
Role.model_rebuild()
UserRoleLink.model_rebuild()
UserCart.model_rebuild()
BaseTimeStampSlugModel.model_rebuild()

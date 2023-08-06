"""
A public swimming pool.

https://schema.org/PublicSwimmingPool
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PublicSwimmingPoolInheritedProperties(TypedDict):
    """A public swimming pool.

    References:
        https://schema.org/PublicSwimmingPool
    Note:
        Model Depth 5
    Attributes:
    """

    


class PublicSwimmingPoolProperties(TypedDict):
    """A public swimming pool.

    References:
        https://schema.org/PublicSwimmingPool
    Note:
        Model Depth 5
    Attributes:
    """

    

#PublicSwimmingPoolInheritedPropertiesTd = PublicSwimmingPoolInheritedProperties()
#PublicSwimmingPoolPropertiesTd = PublicSwimmingPoolProperties()


class AllProperties(PublicSwimmingPoolInheritedProperties , PublicSwimmingPoolProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PublicSwimmingPoolProperties, PublicSwimmingPoolInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PublicSwimmingPool"
    return model
    

PublicSwimmingPool = create_schema_org_model()
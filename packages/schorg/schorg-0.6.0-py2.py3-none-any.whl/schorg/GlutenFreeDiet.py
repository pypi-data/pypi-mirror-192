"""
A diet exclusive of gluten.

https://schema.org/GlutenFreeDiet
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class GlutenFreeDietInheritedProperties(TypedDict):
    """A diet exclusive of gluten.

    References:
        https://schema.org/GlutenFreeDiet
    Note:
        Model Depth 5
    Attributes:
    """

    


class GlutenFreeDietProperties(TypedDict):
    """A diet exclusive of gluten.

    References:
        https://schema.org/GlutenFreeDiet
    Note:
        Model Depth 5
    Attributes:
    """

    

#GlutenFreeDietInheritedPropertiesTd = GlutenFreeDietInheritedProperties()
#GlutenFreeDietPropertiesTd = GlutenFreeDietProperties()


class AllProperties(GlutenFreeDietInheritedProperties , GlutenFreeDietProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[GlutenFreeDietProperties, GlutenFreeDietInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "GlutenFreeDiet"
    return model
    

GlutenFreeDiet = create_schema_org_model()
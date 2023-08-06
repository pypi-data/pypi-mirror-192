"""
X-ray imaging.

https://schema.org/XRay
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class XRayInheritedProperties(TypedDict):
    """X-ray imaging.

    References:
        https://schema.org/XRay
    Note:
        Model Depth 6
    Attributes:
    """

    


class XRayProperties(TypedDict):
    """X-ray imaging.

    References:
        https://schema.org/XRay
    Note:
        Model Depth 6
    Attributes:
    """

    

#XRayInheritedPropertiesTd = XRayInheritedProperties()
#XRayPropertiesTd = XRayProperties()


class AllProperties(XRayInheritedProperties , XRayProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[XRayProperties, XRayInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "XRay"
    return model
    

XRay = create_schema_org_model()
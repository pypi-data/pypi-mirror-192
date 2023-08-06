"""
Radiography is an imaging technique that uses electromagnetic radiation other than visible light, especially X-rays, to view the internal structure of a non-uniformly composed and opaque object such as the human body.

https://schema.org/Radiography
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class RadiographyInheritedProperties(TypedDict):
    """Radiography is an imaging technique that uses electromagnetic radiation other than visible light, especially X-rays, to view the internal structure of a non-uniformly composed and opaque object such as the human body.

    References:
        https://schema.org/Radiography
    Note:
        Model Depth 6
    Attributes:
    """

    


class RadiographyProperties(TypedDict):
    """Radiography is an imaging technique that uses electromagnetic radiation other than visible light, especially X-rays, to view the internal structure of a non-uniformly composed and opaque object such as the human body.

    References:
        https://schema.org/Radiography
    Note:
        Model Depth 6
    Attributes:
    """

    

#RadiographyInheritedPropertiesTd = RadiographyInheritedProperties()
#RadiographyPropertiesTd = RadiographyProperties()


class AllProperties(RadiographyInheritedProperties , RadiographyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[RadiographyProperties, RadiographyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Radiography"
    return model
    

Radiography = create_schema_org_model()
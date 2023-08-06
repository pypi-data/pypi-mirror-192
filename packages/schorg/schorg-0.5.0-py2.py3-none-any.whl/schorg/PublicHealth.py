"""
Branch of medicine that pertains to the health services to improve and protect community health, especially epidemiology, sanitation, immunization, and preventive medicine.

https://schema.org/PublicHealth
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PublicHealthInheritedProperties(TypedDict):
    """Branch of medicine that pertains to the health services to improve and protect community health, especially epidemiology, sanitation, immunization, and preventive medicine.

    References:
        https://schema.org/PublicHealth
    Note:
        Model Depth 5
    Attributes:
    """

    


class PublicHealthProperties(TypedDict):
    """Branch of medicine that pertains to the health services to improve and protect community health, especially epidemiology, sanitation, immunization, and preventive medicine.

    References:
        https://schema.org/PublicHealth
    Note:
        Model Depth 5
    Attributes:
    """

    

#PublicHealthInheritedPropertiesTd = PublicHealthInheritedProperties()
#PublicHealthPropertiesTd = PublicHealthProperties()


class AllProperties(PublicHealthInheritedProperties , PublicHealthProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PublicHealthProperties, PublicHealthInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PublicHealth"
    return model
    

PublicHealth = create_schema_org_model()
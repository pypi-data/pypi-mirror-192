"""
A system of medicine focused on promoting the body's innate ability to heal itself.

https://schema.org/Osteopathic
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OsteopathicInheritedProperties(TypedDict):
    """A system of medicine focused on promoting the body's innate ability to heal itself.

    References:
        https://schema.org/Osteopathic
    Note:
        Model Depth 6
    Attributes:
    """

    


class OsteopathicProperties(TypedDict):
    """A system of medicine focused on promoting the body's innate ability to heal itself.

    References:
        https://schema.org/Osteopathic
    Note:
        Model Depth 6
    Attributes:
    """

    

#OsteopathicInheritedPropertiesTd = OsteopathicInheritedProperties()
#OsteopathicPropertiesTd = OsteopathicProperties()


class AllProperties(OsteopathicInheritedProperties , OsteopathicProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OsteopathicProperties, OsteopathicInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Osteopathic"
    return model
    

Osteopathic = create_schema_org_model()
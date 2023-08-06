"""
A system of medicine based on the principle that a disease can be cured by a substance that produces similar symptoms in healthy people.

https://schema.org/Homeopathic
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HomeopathicInheritedProperties(TypedDict):
    """A system of medicine based on the principle that a disease can be cured by a substance that produces similar symptoms in healthy people.

    References:
        https://schema.org/Homeopathic
    Note:
        Model Depth 6
    Attributes:
    """

    


class HomeopathicProperties(TypedDict):
    """A system of medicine based on the principle that a disease can be cured by a substance that produces similar symptoms in healthy people.

    References:
        https://schema.org/Homeopathic
    Note:
        Model Depth 6
    Attributes:
    """

    

#HomeopathicInheritedPropertiesTd = HomeopathicInheritedProperties()
#HomeopathicPropertiesTd = HomeopathicProperties()


class AllProperties(HomeopathicInheritedProperties , HomeopathicProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HomeopathicProperties, HomeopathicInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Homeopathic"
    return model
    

Homeopathic = create_schema_org_model()
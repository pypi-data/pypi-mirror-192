"""
A specific branch of medical science that is concerned with the diagnosis and treatment of diseases, debilities and provision of care to the aged.

https://schema.org/Geriatric
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class GeriatricInheritedProperties(TypedDict):
    """A specific branch of medical science that is concerned with the diagnosis and treatment of diseases, debilities and provision of care to the aged.

    References:
        https://schema.org/Geriatric
    Note:
        Model Depth 5
    Attributes:
    """

    


class GeriatricProperties(TypedDict):
    """A specific branch of medical science that is concerned with the diagnosis and treatment of diseases, debilities and provision of care to the aged.

    References:
        https://schema.org/Geriatric
    Note:
        Model Depth 5
    Attributes:
    """

    

#GeriatricInheritedPropertiesTd = GeriatricInheritedProperties()
#GeriatricPropertiesTd = GeriatricProperties()


class AllProperties(GeriatricInheritedProperties , GeriatricProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[GeriatricProperties, GeriatricInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Geriatric"
    return model
    

Geriatric = create_schema_org_model()
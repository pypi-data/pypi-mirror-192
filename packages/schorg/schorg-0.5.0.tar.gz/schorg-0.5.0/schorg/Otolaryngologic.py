"""
A specific branch of medical science that is concerned with the ear, nose and throat and their respective disease states.

https://schema.org/Otolaryngologic
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OtolaryngologicInheritedProperties(TypedDict):
    """A specific branch of medical science that is concerned with the ear, nose and throat and their respective disease states.

    References:
        https://schema.org/Otolaryngologic
    Note:
        Model Depth 5
    Attributes:
    """

    


class OtolaryngologicProperties(TypedDict):
    """A specific branch of medical science that is concerned with the ear, nose and throat and their respective disease states.

    References:
        https://schema.org/Otolaryngologic
    Note:
        Model Depth 5
    Attributes:
    """

    

#OtolaryngologicInheritedPropertiesTd = OtolaryngologicInheritedProperties()
#OtolaryngologicPropertiesTd = OtolaryngologicProperties()


class AllProperties(OtolaryngologicInheritedProperties , OtolaryngologicProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OtolaryngologicProperties, OtolaryngologicInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Otolaryngologic"
    return model
    

Otolaryngologic = create_schema_org_model()
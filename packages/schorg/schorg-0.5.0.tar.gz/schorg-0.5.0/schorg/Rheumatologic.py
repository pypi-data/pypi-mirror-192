"""
A specific branch of medical science that deals with the study and treatment of rheumatic, autoimmune or joint diseases.

https://schema.org/Rheumatologic
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class RheumatologicInheritedProperties(TypedDict):
    """A specific branch of medical science that deals with the study and treatment of rheumatic, autoimmune or joint diseases.

    References:
        https://schema.org/Rheumatologic
    Note:
        Model Depth 6
    Attributes:
    """

    


class RheumatologicProperties(TypedDict):
    """A specific branch of medical science that deals with the study and treatment of rheumatic, autoimmune or joint diseases.

    References:
        https://schema.org/Rheumatologic
    Note:
        Model Depth 6
    Attributes:
    """

    

#RheumatologicInheritedPropertiesTd = RheumatologicInheritedProperties()
#RheumatologicPropertiesTd = RheumatologicProperties()


class AllProperties(RheumatologicInheritedProperties , RheumatologicProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[RheumatologicProperties, RheumatologicInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Rheumatologic"
    return model
    

Rheumatologic = create_schema_org_model()
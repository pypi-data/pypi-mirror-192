"""
A specific branch of medical science that pertains to the study of the kidneys and its respective disease states.

https://schema.org/Renal
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class RenalInheritedProperties(TypedDict):
    """A specific branch of medical science that pertains to the study of the kidneys and its respective disease states.

    References:
        https://schema.org/Renal
    Note:
        Model Depth 6
    Attributes:
    """

    


class RenalProperties(TypedDict):
    """A specific branch of medical science that pertains to the study of the kidneys and its respective disease states.

    References:
        https://schema.org/Renal
    Note:
        Model Depth 6
    Attributes:
    """

    

#RenalInheritedPropertiesTd = RenalInheritedProperties()
#RenalPropertiesTd = RenalProperties()


class AllProperties(RenalInheritedProperties , RenalProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[RenalProperties, RenalInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Renal"
    return model
    

Renal = create_schema_org_model()
"""
The invitee will attend.

https://schema.org/RsvpResponseYes
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class RsvpResponseYesInheritedProperties(TypedDict):
    """The invitee will attend.

    References:
        https://schema.org/RsvpResponseYes
    Note:
        Model Depth 5
    Attributes:
    """

    


class RsvpResponseYesProperties(TypedDict):
    """The invitee will attend.

    References:
        https://schema.org/RsvpResponseYes
    Note:
        Model Depth 5
    Attributes:
    """

    

#RsvpResponseYesInheritedPropertiesTd = RsvpResponseYesInheritedProperties()
#RsvpResponseYesPropertiesTd = RsvpResponseYesProperties()


class AllProperties(RsvpResponseYesInheritedProperties , RsvpResponseYesProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[RsvpResponseYesProperties, RsvpResponseYesInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "RsvpResponseYes"
    return model
    

RsvpResponseYes = create_schema_org_model()
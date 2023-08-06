"""
The invitee may or may not attend.

https://schema.org/RsvpResponseMaybe
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class RsvpResponseMaybeInheritedProperties(TypedDict):
    """The invitee may or may not attend.

    References:
        https://schema.org/RsvpResponseMaybe
    Note:
        Model Depth 5
    Attributes:
    """

    


class RsvpResponseMaybeProperties(TypedDict):
    """The invitee may or may not attend.

    References:
        https://schema.org/RsvpResponseMaybe
    Note:
        Model Depth 5
    Attributes:
    """

    

#RsvpResponseMaybeInheritedPropertiesTd = RsvpResponseMaybeInheritedProperties()
#RsvpResponseMaybePropertiesTd = RsvpResponseMaybeProperties()


class AllProperties(RsvpResponseMaybeInheritedProperties , RsvpResponseMaybeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[RsvpResponseMaybeProperties, RsvpResponseMaybeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "RsvpResponseMaybe"
    return model
    

RsvpResponseMaybe = create_schema_org_model()
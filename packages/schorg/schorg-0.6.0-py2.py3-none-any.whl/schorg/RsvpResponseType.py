"""
RsvpResponseType is an enumeration type whose instances represent responding to an RSVP request.

https://schema.org/RsvpResponseType
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class RsvpResponseTypeInheritedProperties(TypedDict):
    """RsvpResponseType is an enumeration type whose instances represent responding to an RSVP request.

    References:
        https://schema.org/RsvpResponseType
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class RsvpResponseTypeProperties(TypedDict):
    """RsvpResponseType is an enumeration type whose instances represent responding to an RSVP request.

    References:
        https://schema.org/RsvpResponseType
    Note:
        Model Depth 4
    Attributes:
    """

    

#RsvpResponseTypeInheritedPropertiesTd = RsvpResponseTypeInheritedProperties()
#RsvpResponseTypePropertiesTd = RsvpResponseTypeProperties()


class AllProperties(RsvpResponseTypeInheritedProperties , RsvpResponseTypeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[RsvpResponseTypeProperties, RsvpResponseTypeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "RsvpResponseType"
    return model
    

RsvpResponseType = create_schema_org_model()
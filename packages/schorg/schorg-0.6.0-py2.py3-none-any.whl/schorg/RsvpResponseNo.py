"""
The invitee will not attend.

https://schema.org/RsvpResponseNo
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class RsvpResponseNoInheritedProperties(TypedDict):
    """The invitee will not attend.

    References:
        https://schema.org/RsvpResponseNo
    Note:
        Model Depth 5
    Attributes:
    """

    


class RsvpResponseNoProperties(TypedDict):
    """The invitee will not attend.

    References:
        https://schema.org/RsvpResponseNo
    Note:
        Model Depth 5
    Attributes:
    """

    

#RsvpResponseNoInheritedPropertiesTd = RsvpResponseNoInheritedProperties()
#RsvpResponseNoPropertiesTd = RsvpResponseNoProperties()


class AllProperties(RsvpResponseNoInheritedProperties , RsvpResponseNoProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[RsvpResponseNoProperties, RsvpResponseNoInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "RsvpResponseNo"
    return model
    

RsvpResponseNo = create_schema_org_model()
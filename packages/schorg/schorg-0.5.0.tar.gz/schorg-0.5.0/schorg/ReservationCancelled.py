"""
The status for a previously confirmed reservation that is now cancelled.

https://schema.org/ReservationCancelled
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ReservationCancelledInheritedProperties(TypedDict):
    """The status for a previously confirmed reservation that is now cancelled.

    References:
        https://schema.org/ReservationCancelled
    Note:
        Model Depth 6
    Attributes:
    """

    


class ReservationCancelledProperties(TypedDict):
    """The status for a previously confirmed reservation that is now cancelled.

    References:
        https://schema.org/ReservationCancelled
    Note:
        Model Depth 6
    Attributes:
    """

    

#ReservationCancelledInheritedPropertiesTd = ReservationCancelledInheritedProperties()
#ReservationCancelledPropertiesTd = ReservationCancelledProperties()


class AllProperties(ReservationCancelledInheritedProperties , ReservationCancelledProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ReservationCancelledProperties, ReservationCancelledInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ReservationCancelled"
    return model
    

ReservationCancelled = create_schema_org_model()
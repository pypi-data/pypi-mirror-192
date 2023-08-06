"""
The status of a reservation when a request has been sent, but not confirmed.

https://schema.org/ReservationPending
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ReservationPendingInheritedProperties(TypedDict):
    """The status of a reservation when a request has been sent, but not confirmed.

    References:
        https://schema.org/ReservationPending
    Note:
        Model Depth 6
    Attributes:
    """

    


class ReservationPendingProperties(TypedDict):
    """The status of a reservation when a request has been sent, but not confirmed.

    References:
        https://schema.org/ReservationPending
    Note:
        Model Depth 6
    Attributes:
    """

    

#ReservationPendingInheritedPropertiesTd = ReservationPendingInheritedProperties()
#ReservationPendingPropertiesTd = ReservationPendingProperties()


class AllProperties(ReservationPendingInheritedProperties , ReservationPendingProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ReservationPendingProperties, ReservationPendingInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ReservationPending"
    return model
    

ReservationPending = create_schema_org_model()
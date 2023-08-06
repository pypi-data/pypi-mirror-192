"""
Enumerated status values for Reservation.

https://schema.org/ReservationStatusType
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ReservationStatusTypeInheritedProperties(TypedDict):
    """Enumerated status values for Reservation.

    References:
        https://schema.org/ReservationStatusType
    Note:
        Model Depth 5
    Attributes:
    """

    


class ReservationStatusTypeProperties(TypedDict):
    """Enumerated status values for Reservation.

    References:
        https://schema.org/ReservationStatusType
    Note:
        Model Depth 5
    Attributes:
    """

    

#ReservationStatusTypeInheritedPropertiesTd = ReservationStatusTypeInheritedProperties()
#ReservationStatusTypePropertiesTd = ReservationStatusTypeProperties()


class AllProperties(ReservationStatusTypeInheritedProperties , ReservationStatusTypeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ReservationStatusTypeProperties, ReservationStatusTypeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ReservationStatusType"
    return model
    

ReservationStatusType = create_schema_org_model()
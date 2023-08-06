"""
The status of a confirmed reservation.

https://schema.org/ReservationConfirmed
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ReservationConfirmedInheritedProperties(TypedDict):
    """The status of a confirmed reservation.

    References:
        https://schema.org/ReservationConfirmed
    Note:
        Model Depth 6
    Attributes:
    """

    


class ReservationConfirmedProperties(TypedDict):
    """The status of a confirmed reservation.

    References:
        https://schema.org/ReservationConfirmed
    Note:
        Model Depth 6
    Attributes:
    """

    

#ReservationConfirmedInheritedPropertiesTd = ReservationConfirmedInheritedProperties()
#ReservationConfirmedPropertiesTd = ReservationConfirmedProperties()


class AllProperties(ReservationConfirmedInheritedProperties , ReservationConfirmedProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ReservationConfirmedProperties, ReservationConfirmedInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ReservationConfirmed"
    return model
    

ReservationConfirmed = create_schema_org_model()
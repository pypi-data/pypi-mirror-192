"""
The status of a reservation on hold pending an update like credit card number or flight changes.

https://schema.org/ReservationHold
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ReservationHoldInheritedProperties(TypedDict):
    """The status of a reservation on hold pending an update like credit card number or flight changes.

    References:
        https://schema.org/ReservationHold
    Note:
        Model Depth 6
    Attributes:
    """

    


class ReservationHoldProperties(TypedDict):
    """The status of a reservation on hold pending an update like credit card number or flight changes.

    References:
        https://schema.org/ReservationHold
    Note:
        Model Depth 6
    Attributes:
    """

    

#ReservationHoldInheritedPropertiesTd = ReservationHoldInheritedProperties()
#ReservationHoldPropertiesTd = ReservationHoldProperties()


class AllProperties(ReservationHoldInheritedProperties , ReservationHoldProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ReservationHoldProperties, ReservationHoldInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ReservationHold"
    return model
    

ReservationHold = create_schema_org_model()
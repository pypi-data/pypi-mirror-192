"""
Used to describe a seat, such as a reserved seat in an event reservation.

https://schema.org/Seat
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SeatInheritedProperties(TypedDict):
    """Used to describe a seat, such as a reserved seat in an event reservation.

    References:
        https://schema.org/Seat
    Note:
        Model Depth 3
    Attributes:
    """

    


class SeatProperties(TypedDict):
    """Used to describe a seat, such as a reserved seat in an event reservation.

    References:
        https://schema.org/Seat
    Note:
        Model Depth 3
    Attributes:
        seatSection: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The section location of the reserved seat (e.g. Orchestra).
        seatNumber: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The location of the reserved seat (e.g., 27).
        seatingType: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The type/class of the seat.
        seatRow: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The row location of the reserved seat (e.g., B).
    """

    seatSection: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    seatNumber: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    seatingType: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    seatRow: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#SeatInheritedPropertiesTd = SeatInheritedProperties()
#SeatPropertiesTd = SeatProperties()


class AllProperties(SeatInheritedProperties , SeatProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SeatProperties, SeatInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Seat"
    return model
    

Seat = create_schema_org_model()
"""
A meeting room, conference room, or conference hall is a room provided for singular events such as business conferences and meetings (source: Wikipedia, the free encyclopedia, see <a href="http://en.wikipedia.org/wiki/Conference_hall">http://en.wikipedia.org/wiki/Conference_hall</a>).<br /><br />See also the <a href="/docs/hotels.html">dedicated document on the use of schema.org for marking up hotels and other forms of accommodations</a>.

https://schema.org/MeetingRoom
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MeetingRoomInheritedProperties(TypedDict):
    """A meeting room, conference room, or conference hall is a room provided for singular events such as business conferences and meetings (source: Wikipedia, the free encyclopedia, see <a href="http://en.wikipedia.org/wiki/Conference_hall">http://en.wikipedia.org/wiki/Conference_hall</a>).<br /><br />See also the <a href="/docs/hotels.html">dedicated document on the use of schema.org for marking up hotels and other forms of accommodations</a>.

    References:
        https://schema.org/MeetingRoom
    Note:
        Model Depth 5
    Attributes:
    """

    


class MeetingRoomProperties(TypedDict):
    """A meeting room, conference room, or conference hall is a room provided for singular events such as business conferences and meetings (source: Wikipedia, the free encyclopedia, see <a href="http://en.wikipedia.org/wiki/Conference_hall">http://en.wikipedia.org/wiki/Conference_hall</a>).<br /><br />See also the <a href="/docs/hotels.html">dedicated document on the use of schema.org for marking up hotels and other forms of accommodations</a>.

    References:
        https://schema.org/MeetingRoom
    Note:
        Model Depth 5
    Attributes:
    """

    

#MeetingRoomInheritedPropertiesTd = MeetingRoomInheritedProperties()
#MeetingRoomPropertiesTd = MeetingRoomProperties()


class AllProperties(MeetingRoomInheritedProperties , MeetingRoomProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MeetingRoomProperties, MeetingRoomInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MeetingRoom"
    return model
    

MeetingRoom = create_schema_org_model()
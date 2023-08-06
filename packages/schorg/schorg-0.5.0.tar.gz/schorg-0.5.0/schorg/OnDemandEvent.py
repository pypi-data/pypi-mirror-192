"""
A publication event, e.g. catch-up TV or radio podcast, during which a program is available on-demand.

https://schema.org/OnDemandEvent
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OnDemandEventInheritedProperties(TypedDict):
    """A publication event, e.g. catch-up TV or radio podcast, during which a program is available on-demand.

    References:
        https://schema.org/OnDemandEvent
    Note:
        Model Depth 4
    Attributes:
        publishedBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An agent associated with the publication event.
        free: (Optional[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]): A flag to signal that the item, event, or place is accessible for free.
        publishedOn: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A broadcast service associated with the publication event.
    """

    publishedBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    free: NotRequired[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]
    publishedOn: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class OnDemandEventProperties(TypedDict):
    """A publication event, e.g. catch-up TV or radio podcast, during which a program is available on-demand.

    References:
        https://schema.org/OnDemandEvent
    Note:
        Model Depth 4
    Attributes:
    """

    

#OnDemandEventInheritedPropertiesTd = OnDemandEventInheritedProperties()
#OnDemandEventPropertiesTd = OnDemandEventProperties()


class AllProperties(OnDemandEventInheritedProperties , OnDemandEventProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OnDemandEventProperties, OnDemandEventInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OnDemandEvent"
    return model
    

OnDemandEvent = create_schema_org_model()
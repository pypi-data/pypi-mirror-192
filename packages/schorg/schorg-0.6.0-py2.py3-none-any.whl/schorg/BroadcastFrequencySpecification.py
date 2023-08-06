"""
The frequency in MHz and the modulation used for a particular BroadcastService.

https://schema.org/BroadcastFrequencySpecification
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BroadcastFrequencySpecificationInheritedProperties(TypedDict):
    """The frequency in MHz and the modulation used for a particular BroadcastService.

    References:
        https://schema.org/BroadcastFrequencySpecification
    Note:
        Model Depth 3
    Attributes:
    """

    


class BroadcastFrequencySpecificationProperties(TypedDict):
    """The frequency in MHz and the modulation used for a particular BroadcastService.

    References:
        https://schema.org/BroadcastFrequencySpecification
    Note:
        Model Depth 3
    Attributes:
        broadcastSignalModulation: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The modulation (e.g. FM, AM, etc) used by a particular broadcast service.
        broadcastSubChannel: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The subchannel used for the broadcast.
        broadcastFrequencyValue: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The frequency in MHz for a particular broadcast.
    """

    broadcastSignalModulation: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    broadcastSubChannel: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    broadcastFrequencyValue: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    

#BroadcastFrequencySpecificationInheritedPropertiesTd = BroadcastFrequencySpecificationInheritedProperties()
#BroadcastFrequencySpecificationPropertiesTd = BroadcastFrequencySpecificationProperties()


class AllProperties(BroadcastFrequencySpecificationInheritedProperties , BroadcastFrequencySpecificationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BroadcastFrequencySpecificationProperties, BroadcastFrequencySpecificationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BroadcastFrequencySpecification"
    return model
    

BroadcastFrequencySpecification = create_schema_org_model()
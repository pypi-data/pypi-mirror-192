"""
Residence type: Gated community.

https://schema.org/GatedResidenceCommunity
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class GatedResidenceCommunityInheritedProperties(TypedDict):
    """Residence type: Gated community.

    References:
        https://schema.org/GatedResidenceCommunity
    Note:
        Model Depth 4
    Attributes:
        accommodationFloorPlan: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A floorplan of some [[Accommodation]].
    """

    accommodationFloorPlan: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class GatedResidenceCommunityProperties(TypedDict):
    """Residence type: Gated community.

    References:
        https://schema.org/GatedResidenceCommunity
    Note:
        Model Depth 4
    Attributes:
    """

    

#GatedResidenceCommunityInheritedPropertiesTd = GatedResidenceCommunityInheritedProperties()
#GatedResidenceCommunityPropertiesTd = GatedResidenceCommunityProperties()


class AllProperties(GatedResidenceCommunityInheritedProperties , GatedResidenceCommunityProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[GatedResidenceCommunityProperties, GatedResidenceCommunityInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "GatedResidenceCommunity"
    return model
    

GatedResidenceCommunity = create_schema_org_model()
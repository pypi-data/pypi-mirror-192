"""
A trial that takes place at multiple centers.

https://schema.org/MultiCenterTrial
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MultiCenterTrialInheritedProperties(TypedDict):
    """A trial that takes place at multiple centers.

    References:
        https://schema.org/MultiCenterTrial
    Note:
        Model Depth 6
    Attributes:
    """

    


class MultiCenterTrialProperties(TypedDict):
    """A trial that takes place at multiple centers.

    References:
        https://schema.org/MultiCenterTrial
    Note:
        Model Depth 6
    Attributes:
    """

    

#MultiCenterTrialInheritedPropertiesTd = MultiCenterTrialInheritedProperties()
#MultiCenterTrialPropertiesTd = MultiCenterTrialProperties()


class AllProperties(MultiCenterTrialInheritedProperties , MultiCenterTrialProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MultiCenterTrialProperties, MultiCenterTrialInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MultiCenterTrial"
    return model
    

MultiCenterTrial = create_schema_org_model()
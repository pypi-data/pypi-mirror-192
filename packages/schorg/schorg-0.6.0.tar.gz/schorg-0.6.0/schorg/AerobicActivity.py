"""
Physical activity of relatively low intensity that depends primarily on the aerobic energy-generating process; during activity, the aerobic metabolism uses oxygen to adequately meet energy demands during exercise.

https://schema.org/AerobicActivity
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AerobicActivityInheritedProperties(TypedDict):
    """Physical activity of relatively low intensity that depends primarily on the aerobic energy-generating process; during activity, the aerobic metabolism uses oxygen to adequately meet energy demands during exercise.

    References:
        https://schema.org/AerobicActivity
    Note:
        Model Depth 5
    Attributes:
    """

    


class AerobicActivityProperties(TypedDict):
    """Physical activity of relatively low intensity that depends primarily on the aerobic energy-generating process; during activity, the aerobic metabolism uses oxygen to adequately meet energy demands during exercise.

    References:
        https://schema.org/AerobicActivity
    Note:
        Model Depth 5
    Attributes:
    """

    

#AerobicActivityInheritedPropertiesTd = AerobicActivityInheritedProperties()
#AerobicActivityPropertiesTd = AerobicActivityProperties()


class AllProperties(AerobicActivityInheritedProperties , AerobicActivityProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AerobicActivityProperties, AerobicActivityInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AerobicActivity"
    return model
    

AerobicActivity = create_schema_org_model()
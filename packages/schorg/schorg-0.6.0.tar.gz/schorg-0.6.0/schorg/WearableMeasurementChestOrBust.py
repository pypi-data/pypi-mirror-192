"""
Measurement of the chest/bust section, for example of a suit

https://schema.org/WearableMeasurementChestOrBust
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableMeasurementChestOrBustInheritedProperties(TypedDict):
    """Measurement of the chest/bust section, for example of a suit

    References:
        https://schema.org/WearableMeasurementChestOrBust
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableMeasurementChestOrBustProperties(TypedDict):
    """Measurement of the chest/bust section, for example of a suit

    References:
        https://schema.org/WearableMeasurementChestOrBust
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableMeasurementChestOrBustInheritedPropertiesTd = WearableMeasurementChestOrBustInheritedProperties()
#WearableMeasurementChestOrBustPropertiesTd = WearableMeasurementChestOrBustProperties()


class AllProperties(WearableMeasurementChestOrBustInheritedProperties , WearableMeasurementChestOrBustProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableMeasurementChestOrBustProperties, WearableMeasurementChestOrBustInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableMeasurementChestOrBust"
    return model
    

WearableMeasurementChestOrBust = create_schema_org_model()
"""
A system of medicine that originated in India over thousands of years and that focuses on integrating and balancing the body, mind, and spirit.

https://schema.org/Ayurvedic
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AyurvedicInheritedProperties(TypedDict):
    """A system of medicine that originated in India over thousands of years and that focuses on integrating and balancing the body, mind, and spirit.

    References:
        https://schema.org/Ayurvedic
    Note:
        Model Depth 6
    Attributes:
    """

    


class AyurvedicProperties(TypedDict):
    """A system of medicine that originated in India over thousands of years and that focuses on integrating and balancing the body, mind, and spirit.

    References:
        https://schema.org/Ayurvedic
    Note:
        Model Depth 6
    Attributes:
    """

    

#AyurvedicInheritedPropertiesTd = AyurvedicInheritedProperties()
#AyurvedicPropertiesTd = AyurvedicProperties()


class AllProperties(AyurvedicInheritedProperties , AyurvedicProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AyurvedicProperties, AyurvedicInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Ayurvedic"
    return model
    

Ayurvedic = create_schema_org_model()
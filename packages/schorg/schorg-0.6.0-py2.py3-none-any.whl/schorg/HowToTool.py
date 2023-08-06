"""
A tool used (but not consumed) when performing instructions for how to achieve a result.

https://schema.org/HowToTool
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HowToToolInheritedProperties(TypedDict):
    """A tool used (but not consumed) when performing instructions for how to achieve a result.

    References:
        https://schema.org/HowToTool
    Note:
        Model Depth 5
    Attributes:
        requiredQuantity: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The required quantity of the item(s).
    """

    requiredQuantity: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    


class HowToToolProperties(TypedDict):
    """A tool used (but not consumed) when performing instructions for how to achieve a result.

    References:
        https://schema.org/HowToTool
    Note:
        Model Depth 5
    Attributes:
    """

    

#HowToToolInheritedPropertiesTd = HowToToolInheritedProperties()
#HowToToolPropertiesTd = HowToToolProperties()


class AllProperties(HowToToolInheritedProperties , HowToToolProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HowToToolProperties, HowToToolInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "HowToTool"
    return model
    

HowToTool = create_schema_org_model()
"""
A supply consumed when performing the instructions for how to achieve a result.

https://schema.org/HowToSupply
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HowToSupplyInheritedProperties(TypedDict):
    """A supply consumed when performing the instructions for how to achieve a result.

    References:
        https://schema.org/HowToSupply
    Note:
        Model Depth 5
    Attributes:
        requiredQuantity: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The required quantity of the item(s).
    """

    requiredQuantity: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    


class HowToSupplyProperties(TypedDict):
    """A supply consumed when performing the instructions for how to achieve a result.

    References:
        https://schema.org/HowToSupply
    Note:
        Model Depth 5
    Attributes:
        estimatedCost: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The estimated cost of the supply or supplies consumed when performing instructions.
    """

    estimatedCost: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#HowToSupplyInheritedPropertiesTd = HowToSupplyInheritedProperties()
#HowToSupplyPropertiesTd = HowToSupplyProperties()


class AllProperties(HowToSupplyInheritedProperties , HowToSupplyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HowToSupplyProperties, HowToSupplyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "HowToSupply"
    return model
    

HowToSupply = create_schema_org_model()
"""
Specifies that a return label will be provided by the seller in the shipping box.

https://schema.org/ReturnLabelInBox
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ReturnLabelInBoxInheritedProperties(TypedDict):
    """Specifies that a return label will be provided by the seller in the shipping box.

    References:
        https://schema.org/ReturnLabelInBox
    Note:
        Model Depth 5
    Attributes:
    """

    


class ReturnLabelInBoxProperties(TypedDict):
    """Specifies that a return label will be provided by the seller in the shipping box.

    References:
        https://schema.org/ReturnLabelInBox
    Note:
        Model Depth 5
    Attributes:
    """

    

#ReturnLabelInBoxInheritedPropertiesTd = ReturnLabelInBoxInheritedProperties()
#ReturnLabelInBoxPropertiesTd = ReturnLabelInBoxProperties()


class AllProperties(ReturnLabelInBoxInheritedProperties , ReturnLabelInBoxProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ReturnLabelInBoxProperties, ReturnLabelInBoxInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ReturnLabelInBox"
    return model
    

ReturnLabelInBox = create_schema_org_model()
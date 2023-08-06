"""
Structured values are used when the value of a property has a more complex structure than simply being a textual value or a reference to another thing.

https://schema.org/StructuredValue
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class StructuredValueInheritedProperties(TypedDict):
    """Structured values are used when the value of a property has a more complex structure than simply being a textual value or a reference to another thing.

    References:
        https://schema.org/StructuredValue
    Note:
        Model Depth 3
    Attributes:
    """

    


class StructuredValueProperties(TypedDict):
    """Structured values are used when the value of a property has a more complex structure than simply being a textual value or a reference to another thing.

    References:
        https://schema.org/StructuredValue
    Note:
        Model Depth 3
    Attributes:
    """

    

#StructuredValueInheritedPropertiesTd = StructuredValueInheritedProperties()
#StructuredValuePropertiesTd = StructuredValueProperties()


class AllProperties(StructuredValueInheritedProperties , StructuredValueProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[StructuredValueProperties, StructuredValueInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "StructuredValue"
    return model
    

StructuredValue = create_schema_org_model()
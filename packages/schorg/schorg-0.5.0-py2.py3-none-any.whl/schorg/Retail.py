"""
The drug's cost represents the retail cost of the drug.

https://schema.org/Retail
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class RetailInheritedProperties(TypedDict):
    """The drug's cost represents the retail cost of the drug.

    References:
        https://schema.org/Retail
    Note:
        Model Depth 6
    Attributes:
    """

    


class RetailProperties(TypedDict):
    """The drug's cost represents the retail cost of the drug.

    References:
        https://schema.org/Retail
    Note:
        Model Depth 6
    Attributes:
    """

    

#RetailInheritedPropertiesTd = RetailInheritedProperties()
#RetailPropertiesTd = RetailProperties()


class AllProperties(RetailInheritedProperties , RetailProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[RetailProperties, RetailInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Retail"
    return model
    

Retail = create_schema_org_model()
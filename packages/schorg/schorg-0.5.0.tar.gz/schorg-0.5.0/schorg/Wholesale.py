"""
The drug's cost represents the wholesale acquisition cost of the drug.

https://schema.org/Wholesale
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WholesaleInheritedProperties(TypedDict):
    """The drug's cost represents the wholesale acquisition cost of the drug.

    References:
        https://schema.org/Wholesale
    Note:
        Model Depth 6
    Attributes:
    """

    


class WholesaleProperties(TypedDict):
    """The drug's cost represents the wholesale acquisition cost of the drug.

    References:
        https://schema.org/Wholesale
    Note:
        Model Depth 6
    Attributes:
    """

    

#WholesaleInheritedPropertiesTd = WholesaleInheritedProperties()
#WholesalePropertiesTd = WholesaleProperties()


class AllProperties(WholesaleInheritedProperties , WholesaleProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WholesaleProperties, WholesaleInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Wholesale"
    return model
    

Wholesale = create_schema_org_model()
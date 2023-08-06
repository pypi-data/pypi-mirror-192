"""
Specifies that product returns must be made at a kiosk.

https://schema.org/ReturnAtKiosk
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ReturnAtKioskInheritedProperties(TypedDict):
    """Specifies that product returns must be made at a kiosk.

    References:
        https://schema.org/ReturnAtKiosk
    Note:
        Model Depth 5
    Attributes:
    """

    


class ReturnAtKioskProperties(TypedDict):
    """Specifies that product returns must be made at a kiosk.

    References:
        https://schema.org/ReturnAtKiosk
    Note:
        Model Depth 5
    Attributes:
    """

    

#ReturnAtKioskInheritedPropertiesTd = ReturnAtKioskInheritedProperties()
#ReturnAtKioskPropertiesTd = ReturnAtKioskProperties()


class AllProperties(ReturnAtKioskInheritedProperties , ReturnAtKioskProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ReturnAtKioskProperties, ReturnAtKioskInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ReturnAtKiosk"
    return model
    

ReturnAtKiosk = create_schema_org_model()
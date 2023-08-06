"""
A store that sells mobile phones and related accessories.

https://schema.org/MobilePhoneStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MobilePhoneStoreInheritedProperties(TypedDict):
    """A store that sells mobile phones and related accessories.

    References:
        https://schema.org/MobilePhoneStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class MobilePhoneStoreProperties(TypedDict):
    """A store that sells mobile phones and related accessories.

    References:
        https://schema.org/MobilePhoneStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#MobilePhoneStoreInheritedPropertiesTd = MobilePhoneStoreInheritedProperties()
#MobilePhoneStorePropertiesTd = MobilePhoneStoreProperties()


class AllProperties(MobilePhoneStoreInheritedProperties , MobilePhoneStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MobilePhoneStoreProperties, MobilePhoneStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MobilePhoneStore"
    return model
    

MobilePhoneStore = create_schema_org_model()
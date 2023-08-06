"""
An electronics store.

https://schema.org/ElectronicsStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ElectronicsStoreInheritedProperties(TypedDict):
    """An electronics store.

    References:
        https://schema.org/ElectronicsStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class ElectronicsStoreProperties(TypedDict):
    """An electronics store.

    References:
        https://schema.org/ElectronicsStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#ElectronicsStoreInheritedPropertiesTd = ElectronicsStoreInheritedProperties()
#ElectronicsStorePropertiesTd = ElectronicsStoreProperties()


class AllProperties(ElectronicsStoreInheritedProperties , ElectronicsStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ElectronicsStoreProperties, ElectronicsStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ElectronicsStore"
    return model
    

ElectronicsStore = create_schema_org_model()
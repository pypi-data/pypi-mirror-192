"""
A computer store.

https://schema.org/ComputerStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ComputerStoreInheritedProperties(TypedDict):
    """A computer store.

    References:
        https://schema.org/ComputerStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class ComputerStoreProperties(TypedDict):
    """A computer store.

    References:
        https://schema.org/ComputerStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#ComputerStoreInheritedPropertiesTd = ComputerStoreInheritedProperties()
#ComputerStorePropertiesTd = ComputerStoreProperties()


class AllProperties(ComputerStoreInheritedProperties , ComputerStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ComputerStoreProperties, ComputerStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ComputerStore"
    return model
    

ComputerStore = create_schema_org_model()
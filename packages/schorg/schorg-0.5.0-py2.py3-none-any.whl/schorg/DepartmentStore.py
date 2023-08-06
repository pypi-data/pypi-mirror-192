"""
A department store.

https://schema.org/DepartmentStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DepartmentStoreInheritedProperties(TypedDict):
    """A department store.

    References:
        https://schema.org/DepartmentStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class DepartmentStoreProperties(TypedDict):
    """A department store.

    References:
        https://schema.org/DepartmentStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#DepartmentStoreInheritedPropertiesTd = DepartmentStoreInheritedProperties()
#DepartmentStorePropertiesTd = DepartmentStoreProperties()


class AllProperties(DepartmentStoreInheritedProperties , DepartmentStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DepartmentStoreProperties, DepartmentStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DepartmentStore"
    return model
    

DepartmentStore = create_schema_org_model()
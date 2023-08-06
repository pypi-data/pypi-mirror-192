"""
Professional service: Attorney. This type is deprecated - [[LegalService]] is more inclusive and less ambiguous.

https://schema.org/Attorney
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AttorneyInheritedProperties(TypedDict):
    """Professional service: Attorney. This type is deprecated - [[LegalService]] is more inclusive and less ambiguous.

    References:
        https://schema.org/Attorney
    Note:
        Model Depth 5
    Attributes:
    """

    


class AttorneyProperties(TypedDict):
    """Professional service: Attorney. This type is deprecated - [[LegalService]] is more inclusive and less ambiguous.

    References:
        https://schema.org/Attorney
    Note:
        Model Depth 5
    Attributes:
    """

    

#AttorneyInheritedPropertiesTd = AttorneyInheritedProperties()
#AttorneyPropertiesTd = AttorneyProperties()


class AllProperties(AttorneyInheritedProperties , AttorneyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AttorneyProperties, AttorneyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Attorney"
    return model
    

Attorney = create_schema_org_model()
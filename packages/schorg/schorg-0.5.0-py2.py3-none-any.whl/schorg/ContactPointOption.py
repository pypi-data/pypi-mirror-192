"""
Enumerated options related to a ContactPoint.

https://schema.org/ContactPointOption
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ContactPointOptionInheritedProperties(TypedDict):
    """Enumerated options related to a ContactPoint.

    References:
        https://schema.org/ContactPointOption
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class ContactPointOptionProperties(TypedDict):
    """Enumerated options related to a ContactPoint.

    References:
        https://schema.org/ContactPointOption
    Note:
        Model Depth 4
    Attributes:
    """

    

#ContactPointOptionInheritedPropertiesTd = ContactPointOptionInheritedProperties()
#ContactPointOptionPropertiesTd = ContactPointOptionProperties()


class AllProperties(ContactPointOptionInheritedProperties , ContactPointOptionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ContactPointOptionProperties, ContactPointOptionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ContactPointOption"
    return model
    

ContactPointOption = create_schema_org_model()
"""
Intended audience for an item, i.e. the group for whom the item was created.

https://schema.org/Audience
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AudienceInheritedProperties(TypedDict):
    """Intended audience for an item, i.e. the group for whom the item was created.

    References:
        https://schema.org/Audience
    Note:
        Model Depth 3
    Attributes:
    """

    


class AudienceProperties(TypedDict):
    """Intended audience for an item, i.e. the group for whom the item was created.

    References:
        https://schema.org/Audience
    Note:
        Model Depth 3
    Attributes:
        audienceType: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The target group associated with a given audience (e.g. veterans, car owners, musicians, etc.).
        geographicArea: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The geographic area associated with the audience.
    """

    audienceType: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    geographicArea: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#AudienceInheritedPropertiesTd = AudienceInheritedProperties()
#AudiencePropertiesTd = AudienceProperties()


class AllProperties(AudienceInheritedProperties , AudienceProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AudienceProperties, AudienceInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Audience"
    return model
    

Audience = create_schema_org_model()
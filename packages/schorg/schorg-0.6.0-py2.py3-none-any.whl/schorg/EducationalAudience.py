"""
An EducationalAudience.

https://schema.org/EducationalAudience
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EducationalAudienceInheritedProperties(TypedDict):
    """An EducationalAudience.

    References:
        https://schema.org/EducationalAudience
    Note:
        Model Depth 4
    Attributes:
        audienceType: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The target group associated with a given audience (e.g. veterans, car owners, musicians, etc.).
        geographicArea: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The geographic area associated with the audience.
    """

    audienceType: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    geographicArea: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class EducationalAudienceProperties(TypedDict):
    """An EducationalAudience.

    References:
        https://schema.org/EducationalAudience
    Note:
        Model Depth 4
    Attributes:
        educationalRole: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): An educationalRole of an EducationalAudience.
    """

    educationalRole: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#EducationalAudienceInheritedPropertiesTd = EducationalAudienceInheritedProperties()
#EducationalAudiencePropertiesTd = EducationalAudienceProperties()


class AllProperties(EducationalAudienceInheritedProperties , EducationalAudienceProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EducationalAudienceProperties, EducationalAudienceInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EducationalAudience"
    return model
    

EducationalAudience = create_schema_org_model()
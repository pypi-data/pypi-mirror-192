"""
Researchers.

https://schema.org/Researcher
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ResearcherInheritedProperties(TypedDict):
    """Researchers.

    References:
        https://schema.org/Researcher
    Note:
        Model Depth 4
    Attributes:
        audienceType: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The target group associated with a given audience (e.g. veterans, car owners, musicians, etc.).
        geographicArea: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The geographic area associated with the audience.
    """

    audienceType: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    geographicArea: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class ResearcherProperties(TypedDict):
    """Researchers.

    References:
        https://schema.org/Researcher
    Note:
        Model Depth 4
    Attributes:
    """

    

#ResearcherInheritedPropertiesTd = ResearcherInheritedProperties()
#ResearcherPropertiesTd = ResearcherProperties()


class AllProperties(ResearcherInheritedProperties , ResearcherProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ResearcherProperties, ResearcherInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Researcher"
    return model
    

Researcher = create_schema_org_model()
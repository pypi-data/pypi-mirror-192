"""
A scholarly article in the medical domain.

https://schema.org/MedicalScholarlyArticle
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MedicalScholarlyArticleInheritedProperties(TypedDict):
    """A scholarly article in the medical domain.

    References:
        https://schema.org/MedicalScholarlyArticle
    Note:
        Model Depth 5
    Attributes:
    """

    


class MedicalScholarlyArticleProperties(TypedDict):
    """A scholarly article in the medical domain.

    References:
        https://schema.org/MedicalScholarlyArticle
    Note:
        Model Depth 5
    Attributes:
        publicationType: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The type of the medical article, taken from the US NLM MeSH publication type catalog. See also [MeSH documentation](http://www.nlm.nih.gov/mesh/pubtypes.html).
    """

    publicationType: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#MedicalScholarlyArticleInheritedPropertiesTd = MedicalScholarlyArticleInheritedProperties()
#MedicalScholarlyArticlePropertiesTd = MedicalScholarlyArticleProperties()


class AllProperties(MedicalScholarlyArticleInheritedProperties , MedicalScholarlyArticleProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MedicalScholarlyArticleProperties, MedicalScholarlyArticleInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MedicalScholarlyArticle"
    return model
    

MedicalScholarlyArticle = create_schema_org_model()
"""
A guideline recommendation that is regarded as efficacious and where quality of the data supporting the recommendation is sound.

https://schema.org/MedicalGuidelineRecommendation
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MedicalGuidelineRecommendationInheritedProperties(TypedDict):
    """A guideline recommendation that is regarded as efficacious and where quality of the data supporting the recommendation is sound.

    References:
        https://schema.org/MedicalGuidelineRecommendation
    Note:
        Model Depth 4
    Attributes:
        evidenceLevel: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Strength of evidence of the data used to formulate the guideline (enumerated).
        guidelineSubject: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The medical conditions, treatments, etc. that are the subject of the guideline.
        guidelineDate: (Optional[Union[List[Union[SchemaOrgObj, str, date]], SchemaOrgObj, str, date]]): Date on which this guideline's recommendation was made.
        evidenceOrigin: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Source of the data used to formulate the guidance, e.g. RCT, consensus opinion, etc.
    """

    evidenceLevel: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    guidelineSubject: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    guidelineDate: NotRequired[Union[List[Union[SchemaOrgObj, str, date]], SchemaOrgObj, str, date]]
    evidenceOrigin: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    


class MedicalGuidelineRecommendationProperties(TypedDict):
    """A guideline recommendation that is regarded as efficacious and where quality of the data supporting the recommendation is sound.

    References:
        https://schema.org/MedicalGuidelineRecommendation
    Note:
        Model Depth 4
    Attributes:
        recommendationStrength: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Strength of the guideline's recommendation (e.g. 'class I').
    """

    recommendationStrength: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#MedicalGuidelineRecommendationInheritedPropertiesTd = MedicalGuidelineRecommendationInheritedProperties()
#MedicalGuidelineRecommendationPropertiesTd = MedicalGuidelineRecommendationProperties()


class AllProperties(MedicalGuidelineRecommendationInheritedProperties , MedicalGuidelineRecommendationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MedicalGuidelineRecommendationProperties, MedicalGuidelineRecommendationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MedicalGuidelineRecommendation"
    return model
    

MedicalGuidelineRecommendation = create_schema_org_model()
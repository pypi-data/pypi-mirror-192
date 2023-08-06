"""
Target audiences for medical web pages.

https://schema.org/MedicalAudience
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MedicalAudienceInheritedProperties(TypedDict):
    """Target audiences for medical web pages.

    References:
        https://schema.org/MedicalAudience
    Note:
        Model Depth 4
    Attributes:
        healthCondition: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Specifying the health condition(s) of a patient, medical study, or other target audience.
        requiredGender: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Audiences defined by a person's gender.
        suggestedMinAge: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): Minimum recommended age in years for the audience or user.
        requiredMinAge: (Optional[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]): Audiences defined by a person's minimum age.
        suggestedMeasurement: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A suggested range of body measurements for the intended audience or person, for example inseam between 32 and 34 inches or height between 170 and 190 cm. Typically found on a size chart for wearable products.
        suggestedGender: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The suggested gender of the intended person or audience, for example "male", "female", or "unisex".
        requiredMaxAge: (Optional[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]): Audiences defined by a person's maximum age.
        suggestedAge: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The age or age range for the intended audience or person, for example 3-12 months for infants, 1-5 years for toddlers.
        suggestedMaxAge: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): Maximum recommended age in years for the audience or user.
        audienceType: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The target group associated with a given audience (e.g. veterans, car owners, musicians, etc.).
        geographicArea: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The geographic area associated with the audience.
    """

    healthCondition: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    requiredGender: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    suggestedMinAge: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    requiredMinAge: NotRequired[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]
    suggestedMeasurement: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    suggestedGender: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    requiredMaxAge: NotRequired[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]
    suggestedAge: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    suggestedMaxAge: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    audienceType: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    geographicArea: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class MedicalAudienceProperties(TypedDict):
    """Target audiences for medical web pages.

    References:
        https://schema.org/MedicalAudience
    Note:
        Model Depth 4
    Attributes:
    """

    

#MedicalAudienceInheritedPropertiesTd = MedicalAudienceInheritedProperties()
#MedicalAudiencePropertiesTd = MedicalAudienceProperties()


class AllProperties(MedicalAudienceInheritedProperties , MedicalAudienceProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MedicalAudienceProperties, MedicalAudienceInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MedicalAudience"
    return model
    

MedicalAudience = create_schema_org_model()
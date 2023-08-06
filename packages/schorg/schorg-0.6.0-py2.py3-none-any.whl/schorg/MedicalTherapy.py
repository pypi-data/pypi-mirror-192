"""
Any medical intervention designed to prevent, treat, and cure human diseases and medical conditions, including both curative and palliative therapies. Medical therapies are typically processes of care relying upon pharmacotherapy, behavioral therapy, supportive therapy (with fluid or nutrition for example), or detoxification (e.g. hemodialysis) aimed at improving or preventing a health condition.

https://schema.org/MedicalTherapy
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MedicalTherapyInheritedProperties(TypedDict):
    """Any medical intervention designed to prevent, treat, and cure human diseases and medical conditions, including both curative and palliative therapies. Medical therapies are typically processes of care relying upon pharmacotherapy, behavioral therapy, supportive therapy (with fluid or nutrition for example), or detoxification (e.g. hemodialysis) aimed at improving or preventing a health condition.

    References:
        https://schema.org/MedicalTherapy
    Note:
        Model Depth 5
    Attributes:
        doseSchedule: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A dosing schedule for the drug for a given population, either observed, recommended, or maximum dose based on the type used.
        drug: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Specifying a drug or medicine used in a medication procedure.
        adverseOutcome: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A possible complication and/or side effect of this therapy. If it is known that an adverse outcome is serious (resulting in death, disability, or permanent damage; requiring hospitalization; or otherwise life-threatening or requiring immediate medical attention), tag it as a seriousAdverseOutcome instead.
    """

    doseSchedule: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    drug: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    adverseOutcome: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class MedicalTherapyProperties(TypedDict):
    """Any medical intervention designed to prevent, treat, and cure human diseases and medical conditions, including both curative and palliative therapies. Medical therapies are typically processes of care relying upon pharmacotherapy, behavioral therapy, supportive therapy (with fluid or nutrition for example), or detoxification (e.g. hemodialysis) aimed at improving or preventing a health condition.

    References:
        https://schema.org/MedicalTherapy
    Note:
        Model Depth 5
    Attributes:
        seriousAdverseOutcome: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A possible serious complication and/or serious side effect of this therapy. Serious adverse outcomes include those that are life-threatening; result in death, disability, or permanent damage; require hospitalization or prolong existing hospitalization; cause congenital anomalies or birth defects; or jeopardize the patient and may require medical or surgical intervention to prevent one of the outcomes in this definition.
        duplicateTherapy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A therapy that duplicates or overlaps this one.
        contraindication: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A contraindication for this therapy.
    """

    seriousAdverseOutcome: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    duplicateTherapy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    contraindication: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#MedicalTherapyInheritedPropertiesTd = MedicalTherapyInheritedProperties()
#MedicalTherapyPropertiesTd = MedicalTherapyProperties()


class AllProperties(MedicalTherapyInheritedProperties , MedicalTherapyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MedicalTherapyProperties, MedicalTherapyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MedicalTherapy"
    return model
    

MedicalTherapy = create_schema_org_model()
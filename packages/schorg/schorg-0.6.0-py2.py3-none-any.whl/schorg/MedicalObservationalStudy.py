"""
An observational study is a type of medical study that attempts to infer the possible effect of a treatment through observation of a cohort of subjects over a period of time. In an observational study, the assignment of subjects into treatment groups versus control groups is outside the control of the investigator. This is in contrast with controlled studies, such as the randomized controlled trials represented by MedicalTrial, where each subject is randomly assigned to a treatment group or a control group before the start of the treatment.

https://schema.org/MedicalObservationalStudy
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MedicalObservationalStudyInheritedProperties(TypedDict):
    """An observational study is a type of medical study that attempts to infer the possible effect of a treatment through observation of a cohort of subjects over a period of time. In an observational study, the assignment of subjects into treatment groups versus control groups is outside the control of the investigator. This is in contrast with controlled studies, such as the randomized controlled trials represented by MedicalTrial, where each subject is randomly assigned to a treatment group or a control group before the start of the treatment.

    References:
        https://schema.org/MedicalObservationalStudy
    Note:
        Model Depth 4
    Attributes:
        studySubject: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A subject of the study, i.e. one of the medical conditions, therapies, devices, drugs, etc. investigated by the study.
        studyLocation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The location in which the study is taking/took place.
        healthCondition: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Specifying the health condition(s) of a patient, medical study, or other target audience.
        status: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The status of the study (enumerated).
        sponsor: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A person or organization that supports a thing through a pledge, promise, or financial contribution. E.g. a sponsor of a Medical Study or a corporate sponsor of an event.
    """

    studySubject: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    studyLocation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    healthCondition: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    status: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    sponsor: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class MedicalObservationalStudyProperties(TypedDict):
    """An observational study is a type of medical study that attempts to infer the possible effect of a treatment through observation of a cohort of subjects over a period of time. In an observational study, the assignment of subjects into treatment groups versus control groups is outside the control of the investigator. This is in contrast with controlled studies, such as the randomized controlled trials represented by MedicalTrial, where each subject is randomly assigned to a treatment group or a control group before the start of the treatment.

    References:
        https://schema.org/MedicalObservationalStudy
    Note:
        Model Depth 4
    Attributes:
        studyDesign: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Specifics about the observational study design (enumerated).
    """

    studyDesign: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#MedicalObservationalStudyInheritedPropertiesTd = MedicalObservationalStudyInheritedProperties()
#MedicalObservationalStudyPropertiesTd = MedicalObservationalStudyProperties()


class AllProperties(MedicalObservationalStudyInheritedProperties , MedicalObservationalStudyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MedicalObservationalStudyProperties, MedicalObservationalStudyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MedicalObservationalStudy"
    return model
    

MedicalObservationalStudy = create_schema_org_model()
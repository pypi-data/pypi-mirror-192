"""
Also known as a panel study. A cohort study is a form of longitudinal study used in medicine and social science. It is one type of study design and should be compared with a cross-sectional study.  A cohort is a group of people who share a common characteristic or experience within a defined period (e.g., are born, leave school, lose their job, are exposed to a drug or a vaccine, etc.). The comparison group may be the general population from which the cohort is drawn, or it may be another cohort of persons thought to have had little or no exposure to the substance under investigation, but otherwise similar. Alternatively, subgroups within the cohort may be compared with each other.

https://schema.org/CohortStudy
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CohortStudyInheritedProperties(TypedDict):
    """Also known as a panel study. A cohort study is a form of longitudinal study used in medicine and social science. It is one type of study design and should be compared with a cross-sectional study.  A cohort is a group of people who share a common characteristic or experience within a defined period (e.g., are born, leave school, lose their job, are exposed to a drug or a vaccine, etc.). The comparison group may be the general population from which the cohort is drawn, or it may be another cohort of persons thought to have had little or no exposure to the substance under investigation, but otherwise similar. Alternatively, subgroups within the cohort may be compared with each other.

    References:
        https://schema.org/CohortStudy
    Note:
        Model Depth 6
    Attributes:
    """

    


class CohortStudyProperties(TypedDict):
    """Also known as a panel study. A cohort study is a form of longitudinal study used in medicine and social science. It is one type of study design and should be compared with a cross-sectional study.  A cohort is a group of people who share a common characteristic or experience within a defined period (e.g., are born, leave school, lose their job, are exposed to a drug or a vaccine, etc.). The comparison group may be the general population from which the cohort is drawn, or it may be another cohort of persons thought to have had little or no exposure to the substance under investigation, but otherwise similar. Alternatively, subgroups within the cohort may be compared with each other.

    References:
        https://schema.org/CohortStudy
    Note:
        Model Depth 6
    Attributes:
    """

    

#CohortStudyInheritedPropertiesTd = CohortStudyInheritedProperties()
#CohortStudyPropertiesTd = CohortStudyProperties()


class AllProperties(CohortStudyInheritedProperties , CohortStudyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CohortStudyProperties, CohortStudyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CohortStudy"
    return model
    

CohortStudy = create_schema_org_model()
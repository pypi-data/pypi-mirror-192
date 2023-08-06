"""
Any rule set or interactive tool for estimating the risk of developing a complication or condition.

https://schema.org/MedicalRiskEstimator
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MedicalRiskEstimatorInheritedProperties(TypedDict):
    """Any rule set or interactive tool for estimating the risk of developing a complication or condition.

    References:
        https://schema.org/MedicalRiskEstimator
    Note:
        Model Depth 3
    Attributes:
        recognizingAuthority: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): If applicable, the organization that officially recognizes this entity as part of its endorsed system of medicine.
        relevantSpecialty: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): If applicable, a medical specialty in which this entity is relevant.
        medicineSystem: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The system of medicine that includes this MedicalEntity, for example 'evidence-based', 'homeopathic', 'chiropractic', etc.
        funding: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A [[Grant]] that directly or indirectly provide funding or sponsorship for this item. See also [[ownershipFundingInfo]].
        legalStatus: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The drug or supplement's legal status, including any controlled substance schedules that apply.
        study: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A medical study or trial related to this entity.
        guideline: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A medical guideline related to this entity.
        code: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A medical code for the entity, taken from a controlled vocabulary or ontology such as ICD-9, DiseasesDB, MeSH, SNOMED-CT, RxNorm, etc.
    """

    recognizingAuthority: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    relevantSpecialty: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    medicineSystem: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    funding: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    legalStatus: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    study: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    guideline: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    code: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class MedicalRiskEstimatorProperties(TypedDict):
    """Any rule set or interactive tool for estimating the risk of developing a complication or condition.

    References:
        https://schema.org/MedicalRiskEstimator
    Note:
        Model Depth 3
    Attributes:
        estimatesRiskOf: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The condition, complication, or symptom whose risk is being estimated.
        includedRiskFactor: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A modifiable or non-modifiable risk factor included in the calculation, e.g. age, coexisting condition.
    """

    estimatesRiskOf: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    includedRiskFactor: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#MedicalRiskEstimatorInheritedPropertiesTd = MedicalRiskEstimatorInheritedProperties()
#MedicalRiskEstimatorPropertiesTd = MedicalRiskEstimatorProperties()


class AllProperties(MedicalRiskEstimatorInheritedProperties , MedicalRiskEstimatorProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MedicalRiskEstimatorProperties, MedicalRiskEstimatorInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MedicalRiskEstimator"
    return model
    

MedicalRiskEstimator = create_schema_org_model()
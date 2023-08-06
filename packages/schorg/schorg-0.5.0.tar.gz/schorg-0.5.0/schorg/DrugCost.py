"""
The cost per unit of a medical drug. Note that this type is not meant to represent the price in an offer of a drug for sale; see the Offer type for that. This type will typically be used to tag wholesale or average retail cost of a drug, or maximum reimbursable cost. Costs of medical drugs vary widely depending on how and where they are paid for, so while this type captures some of the variables, costs should be used with caution by consumers of this schema's markup.

https://schema.org/DrugCost
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DrugCostInheritedProperties(TypedDict):
    """The cost per unit of a medical drug. Note that this type is not meant to represent the price in an offer of a drug for sale; see the Offer type for that. This type will typically be used to tag wholesale or average retail cost of a drug, or maximum reimbursable cost. Costs of medical drugs vary widely depending on how and where they are paid for, so while this type captures some of the variables, costs should be used with caution by consumers of this schema's markup.

    References:
        https://schema.org/DrugCost
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
    


class DrugCostProperties(TypedDict):
    """The cost per unit of a medical drug. Note that this type is not meant to represent the price in an offer of a drug for sale; see the Offer type for that. This type will typically be used to tag wholesale or average retail cost of a drug, or maximum reimbursable cost. Costs of medical drugs vary widely depending on how and where they are paid for, so while this type captures some of the variables, costs should be used with caution by consumers of this schema's markup.

    References:
        https://schema.org/DrugCost
    Note:
        Model Depth 3
    Attributes:
        costPerUnit: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The cost per unit of the drug.
        applicableLocation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The location in which the status applies.
        drugUnit: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The unit in which the drug is measured, e.g. '5 mg tablet'.
        costOrigin: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Additional details to capture the origin of the cost data. For example, 'Medicare Part B'.
        costCategory: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The category of cost, such as wholesale, retail, reimbursement cap, etc.
        costCurrency: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The currency (in 3-letter) of the drug cost. See: http://en.wikipedia.org/wiki/ISO_4217. 
    """

    costPerUnit: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    applicableLocation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    drugUnit: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    costOrigin: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    costCategory: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    costCurrency: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#DrugCostInheritedPropertiesTd = DrugCostInheritedProperties()
#DrugCostPropertiesTd = DrugCostProperties()


class AllProperties(DrugCostInheritedProperties , DrugCostProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DrugCostProperties, DrugCostInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DrugCost"
    return model
    

DrugCost = create_schema_org_model()
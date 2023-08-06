"""
Any part of the human body, typically a component of an anatomical system. Organs, tissues, and cells are all anatomical structures.

https://schema.org/AnatomicalStructure
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AnatomicalStructureInheritedProperties(TypedDict):
    """Any part of the human body, typically a component of an anatomical system. Organs, tissues, and cells are all anatomical structures.

    References:
        https://schema.org/AnatomicalStructure
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
    


class AnatomicalStructureProperties(TypedDict):
    """Any part of the human body, typically a component of an anatomical system. Organs, tissues, and cells are all anatomical structures.

    References:
        https://schema.org/AnatomicalStructure
    Note:
        Model Depth 3
    Attributes:
        connectedTo: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Other anatomical structures to which this structure is connected.
        partOfSystem: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The anatomical or organ system that this structure is part of.
        associatedPathophysiology: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): If applicable, a description of the pathophysiology associated with the anatomical system, including potential abnormal changes in the mechanical, physical, and biochemical functions of the system.
        bodyLocation: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Location in the body of the anatomical structure.
        relatedTherapy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A medical therapy related to this anatomy.
        subStructure: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Component (sub-)structure(s) that comprise this anatomical structure.
        relatedCondition: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A medical condition associated with this anatomy.
        diagram: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An image containing a diagram that illustrates the structure and/or its component substructures and/or connections with other structures.
    """

    connectedTo: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    partOfSystem: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    associatedPathophysiology: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    bodyLocation: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    relatedTherapy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    subStructure: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    relatedCondition: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    diagram: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#AnatomicalStructureInheritedPropertiesTd = AnatomicalStructureInheritedProperties()
#AnatomicalStructurePropertiesTd = AnatomicalStructureProperties()


class AllProperties(AnatomicalStructureInheritedProperties , AnatomicalStructureProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AnatomicalStructureProperties, AnatomicalStructureInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AnatomicalStructure"
    return model
    

AnatomicalStructure = create_schema_org_model()
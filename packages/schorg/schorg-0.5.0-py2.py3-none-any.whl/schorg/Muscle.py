"""
A muscle is an anatomical structure consisting of a contractile form of tissue that animals use to effect movement.

https://schema.org/Muscle
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MuscleInheritedProperties(TypedDict):
    """A muscle is an anatomical structure consisting of a contractile form of tissue that animals use to effect movement.

    References:
        https://schema.org/Muscle
    Note:
        Model Depth 4
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
    


class MuscleProperties(TypedDict):
    """A muscle is an anatomical structure consisting of a contractile form of tissue that animals use to effect movement.

    References:
        https://schema.org/Muscle
    Note:
        Model Depth 4
    Attributes:
        nerve: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The underlying innervation associated with the muscle.
        muscleAction: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The movement the muscle generates.
        bloodSupply: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The blood vessel that carries blood from the heart to the muscle.
        antagonist: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The muscle whose action counteracts the specified muscle.
        insertion: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The place of attachment of a muscle, or what the muscle moves.
    """

    nerve: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    muscleAction: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    bloodSupply: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    antagonist: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    insertion: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#MuscleInheritedPropertiesTd = MuscleInheritedProperties()
#MusclePropertiesTd = MuscleProperties()


class AllProperties(MuscleInheritedProperties , MuscleProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MuscleProperties, MuscleInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Muscle"
    return model
    

Muscle = create_schema_org_model()
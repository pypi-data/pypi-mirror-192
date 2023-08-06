from abc import ABC, abstractmethod
from typing import Mapping, MutableMapping, Sequence, Union, overload

from pywikibot import Claim, ItemPage, LexemePage, PropertyPage

Page = Union[ItemPage, PropertyPage, LexemePage]


class ItemContainer:
    def __init__(self, page: Page):
        self.page = page

    @overload
    def labels(self, language: None = None) -> MutableMapping[str, str]:
        ...

    @overload
    def labels(self, language: str) -> Union[str, None]:
        ...

    def labels(self, language: Union[str, None] = None):
        if language is not None:
            return self.page.labels.get(language, None)
        return self.page.labels

    @overload
    def descriptions(self, language: None = None) -> MutableMapping[str, str]:
        ...

    @overload
    def descriptions(self, language: str) -> Union[str, None]:
        ...

    def descriptions(self, language: Union[str, None] = None):
        if language is not None:
            return self.page.descriptions.get(language, None)
        return self.page.descriptions

    @overload
    def aliases(self, language: None = None) -> MutableMapping[str, list[str]]:
        ...

    @overload
    def aliases(self, language: str) -> list[str]:
        ...

    def aliases(self, language: Union[str, None] = None):
        if language is not None:
            return self.page.aliases.get(language, [])
        return self.page.aliases

    @overload
    def all_titles(self, language: None = None) -> MutableMapping[str, list[str]]:
        ...

    @overload
    def all_titles(self, language: str) -> list[str]:
        ...

    def all_titles(self, language: Union[str, None] = None):
        """Get all titles for the item, with the label first.

        .. note:: An item can have no label and more than zero aliases, so there is no garuntee that the first item
            in the list is the label.
        """
        if language is not None:
            return (
                [self.labels(language)]
                if self.labels(language)
                else [] + self.aliases(language)
            )
        return {
            k: [self.labels(k)] if self.labels(k) else [] + v
            for k, v in self.aliases().items()
        }

    @overload
    def claims(self, property: None = None) -> Mapping[str, "MultiClaimContainer"]:
        ...

    @overload
    def claims(self, property: str) -> "MultiClaimContainer":
        ...

    def claims(self, property: Union[str, None] = None):
        if property is not None:
            val = self.page.claims.get(property, None)
            if val:
                return MultiClaimContainer(val)
            return MultiClaimContainer([])
        return {k: MultiClaimContainer(v) for k, v in self.page.claims.items()}

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self.page!r})"


class ClaimMixin(ABC):
    @property
    @abstractmethod
    def claims(self) -> list[Claim]:
        ...


class SingleClaimContainer(ClaimMixin):
    def __init__(self, claim: Claim):
        self.claim = claim

    @property
    def value(self):
        return self.claim.getTarget()

    @property
    def claims(self) -> list[Claim]:
        return [self.claim]

    @overload
    def qualifiers(self, property: None = None) -> Mapping[str, "MultiClaimContainer"]:
        ...

    @overload
    def qualifiers(self, property: str) -> "MultiClaimContainer":
        ...

    def qualifiers(self, property: Union[str, None] = None):
        if property is not None:
            val = self.claim.qualifiers.get(property, None)
            if val:
                return MultiClaimContainer(val)
            return MultiClaimContainer([])
        return {k: MultiClaimContainer(v) for k, v in self.claim.qualifiers.items()}

    def references(self) -> "MultiReferenceContainer":
        return MultiReferenceContainer(self.claim.sources)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self.claim!r})"


class SingleReferenceContainer:
    def __init__(self, reference_group: MutableMapping[str, list[Claim]]):
        self.reference_group = reference_group

    @overload
    def claims(self, property: None = None) -> Mapping[str, "MultiClaimContainer"]:
        ...

    @overload
    def claims(self, property: str) -> "MultiClaimContainer":
        ...

    def claims(self, property: Union[str, None] = None):
        if property is not None:
            val = self.reference_group.get(property, None)
            if val:
                return MultiClaimContainer(val)
            return MultiClaimContainer([])
        return {k: MultiClaimContainer(v) for k, v in self.reference_group.items()}

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self.reference_group!r})"


class MultiReferenceContainer(Sequence[MutableMapping[str, list[Claim]]]):
    def __init__(self, reference_groups: list[MutableMapping[str, list[Claim]]]):
        self.reference_groups = reference_groups

    def __getitem__(self, index: int) -> SingleReferenceContainer:
        return SingleReferenceContainer(self.reference_groups[index])

    def __len__(self) -> int:
        return len(self.reference_groups)

    def __iter__(self):
        return iter(self.reference_groups)

    def first(self) -> Union[SingleReferenceContainer, None]:
        return (
            SingleReferenceContainer(self.reference_groups[0])
            if self.reference_groups
            else None
        )

    def last(self) -> Union[SingleReferenceContainer, None]:
        return (
            SingleReferenceContainer(self.reference_groups[-1])
            if self.reference_groups
            else None
        )

    @overload
    def claims(
        self, property: None = None
    ) -> list[Mapping[str, "MultiClaimContainer"]]:
        ...

    @overload
    def claims(self, property: str) -> "MultiReferenceClaimContainer":
        ...

    def claims(self, property: Union[str, None] = None):
        if property is not None:
            return MultiReferenceClaimContainer(
                [
                    SingleReferenceContainer(reference).claims(property)
                    for reference in self.reference_groups
                ]
            )
        return [
            SingleReferenceContainer(reference).claims()
            for reference in self.reference_groups
        ]

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self.reference_groups!r})"


class MultiReferenceClaimContainer(list["MultiClaimContainer"]):
    def first_reference_claims(self) -> Union["MultiClaimContainer", None]:
        """Get all the claims of the first reference."""
        return self[0] if self else None

    def last_reference_claims(self) -> Union["MultiClaimContainer", None]:
        """Get all the claims of the last reference."""
        return self[-1] if self else None

    def first(self) -> list[Union[SingleClaimContainer, None]]:
        """Get the first claim of each claim in the list of claims."""
        return [claim.first() for claim in self]

    def last(self) -> list[Union[SingleClaimContainer, None]]:
        """Get the last claim of each claim in the list of claims."""
        return [claim.last() for claim in self]

    def to_claims(self) -> list[list[Claim]]:
        """Convert the MultiReferenceClaimContainer to a list of lists of claims."""
        return [reference.claims for reference in self]

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({super().__repr__()})"


class MultiClaimContainer(ClaimMixin, Sequence[Claim]):
    def __init__(self, claim_list: list[Claim]):
        self.claim_list = claim_list

    @property
    def claims(self) -> list[Claim]:
        return self.claim_list

    def __getitem__(self, index: int) -> Claim:
        return self.claims[index]

    def __len__(self) -> int:
        return len(self.claims)

    def __iter__(self):
        return iter(self.claims)

    @property
    def values(self) -> list:
        return [claim.getTarget() for claim in self.claims]

    def first(self) -> Union[SingleClaimContainer, None]:
        return SingleClaimContainer(self.claims[0]) if self.claims else None

    def last(self) -> Union[SingleClaimContainer, None]:
        return SingleClaimContainer(self.claims[-1]) if self.claims else None

    @overload
    def qualifiers(
        self, property: None = None
    ) -> list[Mapping[str, "MultiClaimContainer"]]:
        ...

    @overload
    def qualifiers(self, property: str) -> "MultiClaimQualifierContainer":
        ...

    def qualifiers(self, property: Union[str, None] = None):
        if property is not None:
            return MultiClaimQualifierContainer(
                [
                    SingleClaimContainer(claim).qualifiers(property)
                    for claim in self.claims
                ]
            )
        return [SingleClaimContainer(claim).qualifiers() for claim in self.claims]

    def references(self) -> "MultiClaimMultiReferenceContainer":
        return MultiClaimMultiReferenceContainer(
            [SingleClaimContainer(claim).references() for claim in self.claims]
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self.claims!r})"


class MultiClaimQualifierContainer(list[MultiClaimContainer]):
    def first_claim_qualifiers(self) -> Union[MultiClaimContainer, None]:
        """Get the qualifiers of the first claim in the list of claims."""
        return self[0] if self else None

    def last_claim_qualifiers(self) -> Union[MultiClaimContainer, None]:
        """Get the qualifiers of the last claim in the list of claims."""
        return self[-1] if self else None

    def first(self) -> list[Union[SingleClaimContainer, None]]:
        """Get the first qualifier of each claim in the list of claims."""
        return [claim.first() for claim in self]

    def last(self) -> list[Union[SingleClaimContainer, None]]:
        """Get the last qualifier of each claim in the list of claims."""
        return [claim.last() for claim in self]

    def to_claims(self) -> list[list[Claim]]:
        """Convert the MultiClaimQualifierContainer to a list of lists of claims."""
        return [claim.claims for claim in self]

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({super().__repr__()})"


class MultiClaimMultiReferenceContainer(list[MultiReferenceContainer]):
    def first_claim_references(self) -> Union[MultiReferenceContainer, None]:
        """Get the references of the first claim in the list of claims."""
        return self[0] if self else None

    def last_claim_references(self) -> Union[MultiReferenceContainer, None]:
        """Get the references of the last claim in the list of claims."""
        return self[-1] if self else None

    def first(self) -> list[Union[SingleClaimContainer, None]]:
        """Get the first reference of each claim in the list of claims."""
        return [claim.first() for claim in self]

    def last(self) -> list[Union[SingleClaimContainer, None]]:
        """Get the last reference of each claim in the list of claims."""
        return [claim.last() for claim in self]

    @overload
    def claims(
        self, property: None = None
    ) -> list[list[Mapping[str, "MultiClaimContainer"]]]:
        ...

    @overload
    def claims(self, property: str) -> "MultiClaimMultiReferenceClaimContainer":
        ...

    def claims(self, property: Union[str, None] = None):
        if property is not None:
            return MultiClaimMultiReferenceClaimContainer(
                [claim.claims(property) for claim in self]
            )
        return [reference.claims() for reference in self]

    def to_reference_groups(self) -> list[list[MutableMapping[str, list[Claim]]]]:
        """Convert the MultiClaimMultiReferenceContainer to a list of reference groups."""
        return [reference.reference_groups for reference in self]

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({super().__repr__()})"


class MultiClaimMultiReferenceClaimContainer(list[MultiReferenceClaimContainer]):
    def first_claim_references_claims(
        self,
    ) -> Union[MultiReferenceClaimContainer, None]:
        """Get the claims of the first reference of the first claim in the list of claims."""
        return self[0] if self else None

    def last_claim_references_claims(self) -> Union[MultiReferenceClaimContainer, None]:
        """Get the claims of the last reference of the last claim in the list of claims."""
        return self[-1] if self else None

    def first(self) -> list[list[Union[SingleClaimContainer, None]]]:
        """Get the first claim of each reference of each claim in the list of claims."""
        return [claim.first() for claim in self]

    def last(self) -> list[list[Union[SingleClaimContainer, None]]]:
        """Get the last claim of each reference of each claim in the list of claims."""
        return [claim.last() for claim in self]

    def to_claims(self) -> list[list[list[Claim]]]:
        """Convert the MultiClaimMultiReferenceClaimContainer to a list of lists of lists of claims."""
        return [reference.to_claims() for reference in self]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({super().__repr__()})"

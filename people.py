from dataclasses import dataclass
from typing import Optional


@dataclass
class Person:
    """
    Data class containing REQUIRED information about individual authors.
    In the XML file, one or more "Person" containers belong inside the "Authors" container element.
    """
    _family_name: str  # Author's surname
    _author_name_paper: str  # Name of author as it appears on title page of paper. Usually "Initials + Surname"
    _author_collaboration: str  #

    @property
    def family_name(self):
        return self._family_name

    @property
    def author_name_paper(self):
        return self._author_name_paper

    @property
    def author_collaboration(self):
        return self._author_collaboration

    def __post_init__(self):
        if not self._family_name:
            raise ValueError("Family name cannot be empty.")
        if not self._author_name_paper:
            raise ValueError("Author name paper cannot be empty.")
        if not self._author_collaboration:
            raise ValueError("Author collaboration cannot be empty.")


@dataclass
class PersonOptions:
    """
    Data class containing OPTIONAL information about individual authors.
    In the XML file, this belongs inside the "Authors" container element.
    """
    initials: Optional[str] = None  # Author's initials for papers
    author_id: Optional[str] = None  # ORCID is preferred
    given_name: Optional[str] = None  # Author's first/given name. Can be blank but generally it's populated.
    author_name_native: Optional[str] = None  # Author's name written in their native language
    author_suffix: Optional[str] = None  # e.g. Jr.,  Sr., III.
    author_status: Optional[str] = None  # Describes vital status of author. If deceased, use "Deceased". Otherwise blank.
    author_name_paper_given: Optional[str] = None  # given name as it appears on title page of paper
    author_name_paper_family: Optional[str] = None  # family name as it appears on title page of paper
    position: Optional[str] = None  # Author's position. May be "Spokesperson", "Contact person", "Speaker" or "Editor".
    author_funding: Optional[str] = None  # Describes the author's funding source, such as a grant or fellowship if necessary

    def __post_init__(self):
        if self.author_status and self.author_status != "Deceased":
            raise ValueError("Author status must be 'Deceased' or None.")

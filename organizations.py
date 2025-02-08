from dataclasses import dataclass
from typing import Optional


@dataclass
class Organization:
    """
    Goes inside the "Organizations" container element.
    Container element with information about an organization with which authors are affiliated.
    There may be one or more organizations within the Organizations container, and each organization
    is identified by the 'id' attribute.
    """
    name: str  # Name of the organization as it will appear on the document.
    org_domain: Optional[str] = None  # OPT: Persistent web address for organization
    org_name: Optional[str] = None  # OPT: name in format of INSPIRE, ROR, etc. Specify with "source" (below).
    org_status: Optional[str] = "Member"  # OPT: status of organization within collaboration. Typically, “member” or “nonmember.”
    org_address: Optional[str] = None  # OPT: Full address of institution as it would be written on letter head.

    def __post_init__(self):
        if not self.name:
            raise ValueError("Organization name cannot be empty.")
        if self.org_status not in ["Member", "Nonmember"]:
            raise ValueError("Organization status must be either 'Member' or 'Nonmember'.")

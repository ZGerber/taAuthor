from dataclasses import dataclass
from typing import Optional


@dataclass
class Collaboration:
    """
    Container element with information about the collaboration.
    In the XML file, this belongs inside the "Collaborations" container element.
    """
    name: str = "TELESCOPE-ARRAY"  # Name of the collaboration.
    id: str = "c1"  # OPT: Is only needed if two (2) or more collaborations publish together.
    group: Optional[str] = None  # OPT: can be used for collaborations wishing to group institutions together
    experiment_number: Optional[str] = None  # OPT: For experiments within collaboration, e.g. TALE, TAX4

    def __post_init__(self):
        if not self.name:
            raise ValueError("Collaboration name cannot be empty.")
        if not self.id:
            raise ValueError("Collaboration id cannot be empty.")

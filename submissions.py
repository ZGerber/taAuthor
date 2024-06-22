from datetime import datetime as dt
from dataclasses import dataclass


@dataclass
class Submission:
    """
    Data class containing submission-specific information.
    """
    _publication_reference: str  # Can be internal report number, arXiv number, ISBN, DOI, web destination, title
    _creation_date: dt = dt.now()
    is_multicollab: bool = False  # Change to TRUE if multiple collaborations publishing together.

    @property
    def publication_reference(self):
        """
        Returns the publication reference as a string
        """
        return self._publication_reference

    @property
    def creation_date(self):
        """
        Returns the creation date as a datetime object.
        """
        return self._creation_date

    @creation_date.setter
    def creation_date(self, date):
        """
        Sets creation_date attribute to 'date'. Useful if you don't want the creation date to be today.
        """
        self._creation_date = date

    @property
    def creation_date_str(self):
        """
        Returns the creation date as a string.
        """
        return self.creation_date.strftime("%Y-%m-%d")

    def __post_init__(self):
        """
        This feature is not yet complete.
        """
        if self.is_multicollab:
            print("ERROR: Multi-collaboration not yet implemented.")


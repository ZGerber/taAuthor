#!/usr/bin/env python3

from dataclasses import dataclass, field
from datetime import datetime as dt
from pathlib import Path
from typing import Optional, List, Tuple, Dict
import xml.etree.ElementTree as et
import argparse
import csv
import re

__author__      = 'Zane Gerber'
__copyright__   = ''
__credits__     = ''
__license__     = ''
__version__     = '1.1.0'
__maintainer__  = 'Zane Gerber'
__email__       = 'zane.gerber@utah.edu'
__status__      = 'Development'


def load_author_csv_list(filename: Path) -> List[dict]:
    """
    Read in the CSV-formatted author list and return entries in a list.
    """
    return list(csv.DictReader(open(filename)))


def load_author_csv_dr(file: str) -> csv.DictReader:
    """
    Read in the CSV-formatted author list and return a DictReader object.
    """
    return csv.DictReader(open(file))


def get_institution_codes(authors: List[dict]) -> List[List[str]]:
    """
    Get the institution codes for all authors in the CSV file.
    Returns a list of lists, since some authors belong to more than one institution.
    This list can then be passed to get_unique_institution_codes().
    """
    return [a['Institution Code'].split(',') for a in authors]


def get_institution_addresses(authors: List[dict]) -> List[List[str]]:
    """
    Get the institution addresses for all authors in the CSV file.
    Returns a list of lists, since some authors belong to more than one institution.
    """
    return [a['Institution'] for a in authors]


def get_institution_dict(institution_codes: List[List[str]], 
                         institution_addresses: List[List[str]]) -> Dict[str, str]:
    """
    Return a dictionary where each key is an institution code and the value is the corresponding institution address.
    """
    inst_dict = {}
    for code, inst in zip(institution_codes, institution_addresses):
        for c in code:
            # Regex to find strings between curly braces
            for i in re.findall(r'\{(?:[^{}])*\}', inst):
                # Remove curly braces from string and define the dictionary item
                inst_dict[c.strip()] = i[1:-1]
    return inst_dict


def get_unique_institution_codes(institutions: List[List[str]]) -> List[str]:
    """
    Get a list of unique institution codes. Removes duplicates, so that each institution is represented only once.
    """
    return list(set(auth_inst.strip() for auth_institutions in institutions for auth_inst in auth_institutions))


def get_number_of_institutions(unique_institutions: List[str]) -> int:
    """
    Get the number of institutions in the collaboration
    """
    return len(unique_institutions)


def get_number_of_authors(authors: List[dict]) -> int:
    """
    Get the number of authors in the collaboration
    """
    return len(authors)


def create_ce(namespace: str,
              ce_name: str,
              **kwargs) -> et.Element:
    """
    This function creates an XML container element with a given namespace and name.
    IMPORTANT: These namespaces and container names must match the INSPIRE convention.
    """
    return et.Element(f"{namespace}:{ce_name}", kwargs)


def create_sub_ce(parent_ce_name: et.Element,
                  namespace: str,
                  sub_ce_name: str,
                  **kwargs) -> et.SubElement:
    """
    This function creates an XML sub-container element with a given namespace and name.
    IMPORTANT: These namespaces and container names must match the INSPIRE convention.
    """
    return et.SubElement(parent_ce_name, f"{namespace}:{sub_ce_name}", kwargs)


def assign_institution_ids(unique_institutions: List[str]) -> dict:
    """
    Assign a unique identifier to each institution in the collaboration.
    This identifier tracks the institution throughout the XML file and is useful for grouping.
    """
    return {inst: f"a{i}" for i, inst in enumerate(unique_institutions, 1)}


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


def parse_user_args() -> argparse.Namespace:
    """
    Parse user-supplied CL arguments
    """
    parser = argparse.ArgumentParser(prog='create_xml.py',
                                     description="Converts author list to XML format using INSPIRE formatting "
                                                 "standards.Default settings are for general use, but this should be "
                                                 "used on a publication-by-publication basis. Required argument is "
                                                 "a publication reference. There is also an option for "
                                                 "multi-collaboration submissions.",
                                     epilog="Developed by Z.Gerber July 2023")
    parser.add_argument('infile', type=str, metavar="infile", help="/full/path/to/authorlist.csv")
    parser.add_argument('-m', '--multi-collab',
                        help="Use this option if more than one collaboration is publishing together on the same paper."
                             "NOTE: This doesn't do anything, yet!",
                        action="store_true")
    parser.add_argument('publication_reference', type=str, metavar="publication-reference",
                        help="Anything that identifies the referenced document. If no immediate identifier, "
                             "the title can be used. Can be internal report number, arXiv number, "
                             "ISBN, DOI, web destination, title.")
    parser.add_argument('-p', '--pretty', 
                        help="Choose not to 'pretty print' the XML author list when saving. Saves one continues chunk of text, which is less readable for humans but fine for XML readers.",
                        action="store_false")
    return parser.parse_args()


def _pretty_print(current: et.ElementTree, parent: et.Element=None, index: int=-1, depth:int=0) -> None:
    """
    Reformat the XML tree. Pretty print by adding whitespace and new lines.
    Code copied from https://stackoverflow.com/questions/28813876/how-do-i-get-pythons-elementtree-to-pretty-print-to-an-xml-file
    This can be relpaced with the et.indent() method if using python version >=3.9
    """
    for i, node in enumerate(current):
        _pretty_print(node, current, i, depth + 1)
    if parent is not None:
        if index == 0:
            parent.text = '\n' + ('\t' * depth)
        else:
            parent[index - 1].tail = '\n' + ('\t' * depth)
        if index == len(parent) - 1:
            current.tail = '\n' + ('\t' * (depth - 1))


def create_and_fill_submission_info(user_args) -> Tuple[et.Element, et.Element]:
    submission = Submission(user_args.publication_reference)
    creationDate = create_sub_ce(root, "cal", "creationDate")
    creationDate.text = submission.creation_date_str
    publicationReference = create_sub_ce(root, "cal", "publicationReference")
    publicationReference.text = submission.publication_reference
    return creationDate, publicationReference


def main() -> None:
    # Read CSV File
    # Loop over authors
    # Create data containers
    # Fill data containers with author info
    # Write to XML file
    return


if __name__ == "__main__":
    # main()

    # These namespaces are required for the INSPIRE format
    et.register_namespace('cal', "http://inspirehep.net/info/HepNames/tools/authors_xml/")
    et.register_namespace('foaf', "http://xmlns.com/foaf/0.1/")
    
    # Parse command-line arguments
    args = parse_user_args()
    
    # Set up ElementTree root
    root = et.Element("collaborationauthorlist")

    # These namespaces are required for the INSPIRE format
    root.set("xmlns:cal","http://inspirehep.net/info/HepNames/tools/authors_xml/")
    root.set("xmlns:foaf", "http://xmlns.com/foaf/0.1/")

    # Load the CSV file
    author_list_file = load_author_csv_list(args.infile)

    # Get institution codes and assign unique IDs to them
    institution_codes_by_auth = get_institution_codes(author_list_file)
    institution_codes = get_unique_institution_codes(institution_codes_by_auth)
    institution_addresses = get_institution_addresses(author_list_file)
    institution_ids = assign_institution_ids(institution_codes)
    inst_dict = get_institution_dict(institution_codes_by_auth, institution_addresses)

    # Count authors and institutions
    n_authors = get_number_of_authors(author_list_file)
    n_institutions = get_number_of_institutions(institution_codes)

    ####################################
    # CREATE & FILL CONTAINER ELEMENTS #
    ####################################
    creationDate, publicationReference = create_and_fill_submission_info(args)
    
    # Collaboration data (i.e. info about TA)
    c = Collaboration()
    collaborations = create_sub_ce(root, "cal", "collaborations")
    collaboration = create_sub_ce(collaborations, "cal", "collaboration", id=c.id)
    collaboration_name = create_sub_ce(collaboration, "foaf", "name")
    collaboration_name.text = c.name
    # experiment_number = create_sub_ce(collaboration, "cal", "experimentNumber") # Not using this for now.

    # Organizations:
    organizations = create_sub_ce(root, "cal", "organizations")
    for code, inst in inst_dict.items():
        org = Organization(name=inst)
        organization = create_sub_ce(organizations, "foaf", "Organization", id=institution_ids[f'{code}'])
        orgDomain = create_sub_ce(organization, "cal", "orgDomain")
        name = create_sub_ce(organization, "foaf", "name")
        name.text = org.name
        orgName = create_sub_ce(organization, "cal", "orgName", source="INSPIRE")
        orgName = create_sub_ce(organization, "cal", "orgName", source="ROR")
        orgName = create_sub_ce(organization, "cal", "orgName", source="INTERNAL")
        orgStatus = create_sub_ce(organization, "cal", "orgStatus", collaborationid="c1")
        orgStatus.text = org.org_status
        orgAddress = create_sub_ce(organization, "cal", "orgAddress")

    # People
    authors = create_sub_ce(root, "cal", "authors")
    for auth, institution in zip(author_list_file, institution_codes_by_auth):
        paper_name_string = auth['Initials'] + " " + auth['Surname']
        person_req = Person(auth['Surname'], ' '.join(paper_name_string.split()), "c1", )
        person_opt = PersonOptions(initials=auth['Initials'],
                                   author_id=auth['ORCID'],
                                   given_name=auth['Given Name'],
                                   author_name_paper_given=auth['Initials'],
                                   author_name_paper_family=auth['Surname'], )

        person = create_sub_ce(authors, "foaf", "Person")

        name = create_sub_ce(person, "foaf", "name")
        name_str = person_opt.given_name + " " + person_req.family_name
        name.text = ' '.join(name_str.split())

        authorNameNative = create_sub_ce(person, "cal", "authorNameNative")

        givenName = create_sub_ce(person, "foaf", "givenName")
        givenName.text = person_opt.given_name

        familyName = create_sub_ce(person, "foaf", "familyName")
        familyName.text = person_req.family_name

        authorSuffix = create_sub_ce(person, "cal", "authorSuffix")

        authorStatus = create_sub_ce(person, "cal", "authorStatus")

        authorNamePaper = create_sub_ce(person, "cal", "authorNamePaper")
        authorNamePaper_str = person_opt.initials + " " + person_req.family_name
        authorNamePaper.text = ' '.join(authorNamePaper_str.split())

        authorNamePaperGiven = create_sub_ce(person, "cal", "authorNamePaperGiven")
        authorNamePaperGiven.text = person_opt.initials

        authorNamePaperFamily = create_sub_ce(person, "cal", "authorNamePaperFamily")
        authorNamePaperFamily.text = person_req.family_name

        authorCollaboration = create_sub_ce(person, "cal", "authorCollaboration", collaborationid="c1")

        authorAffiliations = create_sub_ce(person, "cal", "authorAffiliations")
        for inst in institution:
            authorAffiliation = create_sub_ce(authorAffiliations, "cal", "authorAffiliation",
                                              organizationid=institution_ids[f"{inst.strip()}"],
                                              connection="")

        authorids = create_sub_ce(person, "cal", "authorids")
        authorid = create_sub_ce(authorids, "cal", "authorid", source="ORCID")
        authorid.text = person_opt.author_id

        authorFunding = create_sub_ce(person, "cal", "authorFunding")

    if args.pretty:
        _pretty_print(root)
    tree = et.ElementTree(root)

    ROOT_DIR = Path(__file__).resolve(strict=True).parent
    date_str = creationDate.text.replace('-', '')
    Path(ROOT_DIR / date_str).mkdir(exist_ok=True)
    output_file = ROOT_DIR / date_str / f"{publicationReference.text.replace(' ', '')}.{date_str}.authorlist.xml"
    
    with open(output_file, "wb") as f:
        if args.pretty:
            f.write('<?xml version="1.0" encoding="UTF-8" ?>\n<!DOCTYPE collaborationauthorlist SYSTEM "author.dtd">\n\n'.encode('utf8'))
        else:
            f.write('<?xml version="1.0" encoding="UTF-8" ?><!DOCTYPE collaborationauthorlist SYSTEM "author.dtd">'.encode('utf8'))
        tree.write(f, 'utf-8')

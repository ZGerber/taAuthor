from typing import List, Dict
import xml.etree.ElementTree as et

import submissions
import collaborations
import organizations
import people
from xml_utils import (
    get_institution_codes,
    get_institution_addresses,
    get_institution_dict,
    assign_institution_ids,
    get_unique_institution_codes,
    setup_root_element,
    create_sub_ce,
    create_text_sub_ce)


class AuthorListXMLBuilder:
    def __init__(self, author_list: List[dict], publication_reference: str):
        self.author_list = author_list
        self.publication_reference = publication_reference
        self.institution_codes = get_institution_codes(author_list)
        self.institution_addresses = get_institution_addresses(author_list)
        self.inst_dict = get_institution_dict(self.institution_codes, self.institution_addresses)
        self.institution_ids = assign_institution_ids(get_unique_institution_codes(self.institution_codes))

    def build_tree(self) -> et.ElementTree:
        root = setup_root_element()
        self._add_submission(root)
        self._add_collaboration(root)
        self._add_organizations(root)
        self._add_authors(root)
        return et.ElementTree(root)

    def _add_submission(self, root: et.Element):
        submission = submissions.Submission(self.publication_reference)
        create_text_sub_ce(root, "cal", "creationDate", submission.creation_date_str)
        create_text_sub_ce(root, "cal", "publicationReference", submission.publication_reference)

    @staticmethod
    def _add_collaboration(root: et.Element):
        collab = collaborations.Collaboration()
        collab_parent = create_sub_ce(root, "cal", "collaborations")
        collab_entry = create_sub_ce(collab_parent, "cal", "collaboration", id=collab.id)
        create_text_sub_ce(collab_entry, "foaf", "name", collab.name)

    def _add_organizations(self, root: et.Element):
        orgs = create_sub_ce(root, "cal", "organizations")
        for code, name in self.inst_dict.items():
            org = organizations.Organization(name=name)
            org_el = create_sub_ce(orgs, "foaf", "Organization", id=self.institution_ids[code])
            if org.org_domain:
                create_text_sub_ce(org_el, "cal", "orgDomain", org.org_domain)
            create_text_sub_ce(org_el, "foaf", "name", org.name)
            create_sub_ce(org_el, "cal", "orgName", source="INSPIRE")
            create_sub_ce(org_el, "cal", "orgName", source="ROR")
            create_sub_ce(org_el, "cal", "orgName", source="INTERNAL")
            create_text_sub_ce(org_el, "cal", "orgStatus", org.org_status, collaborationid="c1")
            if org.org_address:
                create_text_sub_ce(org_el, "cal", "orgAddress", org.org_address)

    def _add_authors(self, root: et.Element):
        authors_el = create_sub_ce(root, "cal", "authors")
        for auth, inst_codes in zip(self.author_list, self.institution_codes):
            person_req = people.Person(auth['Surname'], f"{auth['Initials']} {auth['Surname']}", "c1")
            person_opt = people.PersonOptions(
                initials=auth['Initials'],
                author_id=auth['ORCID'],
                given_name=auth['Given Name'],
                author_name_paper_given=auth['Initials'],
                author_name_paper_family=auth['Surname'])

            person_el = create_sub_ce(authors_el, "foaf", "Person")
            create_text_sub_ce(person_el, "foaf", "name", f"{person_opt.given_name} {person_req.family_name}")
            create_text_sub_ce(person_el, "foaf", "givenName", person_opt.given_name)
            create_text_sub_ce(person_el, "foaf", "familyName", person_req.family_name)

            create_text_sub_ce(person_el, "cal", "authorNamePaper", f"{person_opt.initials} {person_req.family_name}")
            create_text_sub_ce(person_el, "cal", "authorNamePaperGiven", person_opt.initials)
            create_text_sub_ce(person_el, "cal", "authorNamePaperFamily", person_req.family_name)
            create_sub_ce(person_el, "cal", "authorCollaboration", collaborationid="c1")

            affs = create_sub_ce(person_el, "cal", "authorAffiliations")
            for inst_code in inst_codes:
                create_sub_ce(affs, "cal", "authorAffiliation", organizationid=self.institution_ids[inst_code.strip()], connection="")

            if person_opt.author_id:
                ids = create_sub_ce(person_el, "cal", "authorids")
                create_text_sub_ce(ids, "cal", "authorid", person_opt.author_id, source="ORCID")

            if person_opt.author_name_native:
                create_text_sub_ce(person_el, "cal", "authorNameNative", person_opt.author_name_native)
            if person_opt.author_suffix:
                create_text_sub_ce(person_el, "cal", "authorSuffix", person_opt.author_suffix)
            if person_opt.author_status:
                create_text_sub_ce(person_el, "cal", "authorStatus", person_opt.author_status)
            if person_opt.author_funding:
                create_text_sub_ce(person_el, "cal", "authorFunding", person_opt.author_funding)

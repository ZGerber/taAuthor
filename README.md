# taAuthor
Create XML Author List using INSPIRE HEP format.

## Background & Motivation
From https://github.com/inspirehep/author.xml:
"Together, INSPIRE, the American Physical Society and arXiv.org have created a template file that you are recommended to use when you provide information about the authors for the submission of your paper. By utilizing unique ID's for authors and organizations (e.g. INSPIRE ID, ORCID, ROR), not only will your authors' information be precise and universally understood, but author information linking to professional information — affiliations, grants, publications, peer review, and more will get exposed.

We recommend that when submitting your document, you also submit an authorlist file called author.xml. Large collaborations with hundreds and even thousands of authors are already using the author.xml file to enable cataloguers and automated processes to glean complete, accurate information on authors. So, let's all be "on the same page" and ensure that authors get recognition for their contributions."

Usage:
```bash
create_xml.py /full/path/to/authorlist.csv "Publication Reference"
```
"Publication Reference" can be an internal report number, arXiv number, ISBN, DOI, web destination, title, etc.

For more see:
```bash
create_xml.py --help 
```

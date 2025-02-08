# taAuthor
Create XML Author List using INSPIRE HEP format.

## Background & Motivation
From https://github.com/inspirehep/author.xml:
"Together, INSPIRE, the American Physical Society and arXiv.org have created a template file that you are recommended to use when you provide information about the authors for the submission of your paper. By utilizing unique ID's for authors and organizations (e.g. INSPIRE ID, ORCID, ROR), not only will your authors' information be precise and universally understood, but author information linking to professional information — affiliations, grants, publications, peer review, and more will get exposed.

We recommend that when submitting your document, you also submit an authorlist file called author.xml. Large collaborations with hundreds and even thousands of authors are already using the author.xml file to enable cataloguers and automated processes to glean complete, accurate information on authors. So, let's all be "on the same page" and ensure that authors get recognition for their contributions."

## Guide
Usage:
```bash
create_xml.py /full/path/to/authorlist.csv "Publication Reference"
```
"Publication Reference" can be an internal report number, arXiv number, ISBN, DOI, web destination, title, etc.

For more see:
```bash
create_xml.py --help 
```

## Code Structure

### `create_xml.py`
This script is the main entry point for creating the XML author list. It reads the CSV file, processes the data, and generates the XML file.

Functions:
- `load_author_csv_list(filename: Path) -> List[dict]`: Reads the CSV-formatted author list and returns entries in a list.
- `load_author_csv_dr(file: str) -> csv.DictReader`: Reads the CSV-formatted author list and returns a DictReader object.
- `get_institution_codes(authors: List[dict]) -> List[List[str]]`: Gets the institution codes for all authors in the CSV file.
- `get_institution_addresses(authors: List[dict]) -> List[List[str]]`: Gets the institution addresses for all authors in the CSV file.
- `get_institution_dict(institution_codes: List[List[str]], institution_addresses: List[List[str]]) -> Dict[str, str]`: Returns a dictionary where each key is an institution code and the value is the corresponding institution address.
- `get_unique_institution_codes(institutions: List[List[str]]) -> List[str]`: Gets a list of unique institution codes.
- `get_number_of_institutions(unique_institutions: List[str]) -> int`: Gets the number of institutions in the collaboration.
- `get_number_of_authors(authors: List[dict]) -> int`: Gets the number of authors in the collaboration.
- `create_ce(namespace: str, ce_name: str, **kwargs) -> et.Element`: Creates an XML container element with a given namespace and name.
- `create_sub_ce(parent_ce_name: et.Element, namespace: str, sub_ce_name: str, **kwargs) -> et.SubElement`: Creates an XML sub-container element with a given namespace and name.
- `assign_institution_ids(unique_institutions: List[str]) -> dict`: Assigns a unique identifier to each institution in the collaboration.
- `parse_user_args() -> argparse.Namespace`: Parses user-supplied command-line arguments.
- `_pretty_print(current: et.ElementTree, parent: et.Element = None, index: int = -1, depth: int = 0) -> None`: Reformats the XML tree for pretty printing.
- `create_and_fill_submission_info(user_args) -> Tuple[et.Element, et.Element]`: Creates and fills submission information elements.
- `main() -> None`: The main function that orchestrates the entire process.

### `collaborations.py`
Defines the `Collaboration` data class, which contains information about the collaboration.

### `organizations.py`
Defines the `Organization` data class, which contains information about an organization with which authors are affiliated.

### `people.py`
Defines the `Person` and `PersonOptions` data classes, which contain information about individual authors.

### `submissions.py`
Defines the `Submission` data class, which contains submission-specific information.

### `author.dtd`
Defines the XML structure for the author list.

## Usage Examples

### Basic Usage
To create an XML author list from a CSV file:
```bash
create_xml.py /full/path/to/authorlist.csv "Publication Reference"
```

### Multi-Collaboration Usage
If more than one collaboration is publishing together on the same paper:
```bash
create_xml.py /full/path/to/authorlist.csv "Publication Reference" --multi-collab
```

### Pretty Print
To pretty print the XML author list when saving:
```bash
create_xml.py /full/path/to/authorlist.csv "Publication Reference" --pretty
```

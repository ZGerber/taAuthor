# taAuthor

Generate `author.xml` files for journal submissions using the INSPIRE HEP format.

## 🧾 Overview

`taAuthor` is a modular Python tool that converts a CSV-formatted author list into a valid XML file conforming to the INSPIRE HEP `author.dtd` specification. This format is required by many journals and repositories, including arXiv and APS, to ensure proper indexing of authors, affiliations, and collaborations.

This tool is designed for large collaborations like Telescope Array and supports:

- Unique institution IDs
- Multiple affiliations per author
- ORCID-based author identification
- Properly structured XML with optional pretty printing

## 🔧 Requirements

- Python 3.7+
- No external libraries required (uses `xml.etree.ElementTree` and Python stdlib)

## 📦 File Structure

- `create_xml.py` — CLI script to generate the XML.
- `collaborations.py` — Defines the collaboration structure (e.g., TA, TAx4).
- `organizations.py` — Parses institutional metadata.
- `people.py` — Handles author data and optional fields.
- `submissions.py` — Tracks publication metadata and submission date.
- `author.dtd` — DTD declaration for XML validation (included in output).
- `README.md` — You are here.

## 🚀 Usage

Run from the command line:

```bash
python create_xml.py /full/path/to/authorlist.csv "Publication Reference"
```

### Example

```bash
python create_xml.py authors.csv "TA Internal Note 2025-04"
```

### Optional Flags

- `--multi-collab`  
  Reserved for future support of multi-collaboration papers. Not yet implemented.

- `--pretty`  
  Pretty-print the XML output for human readability (default). Use `--no-pretty` to output a compact XML string.

### Output

The script creates a subdirectory named by the current date (`YYYYMMDD`) and saves the file as:

```
PublicationReference.YYYYMMDD.authorlist.xml
```

The file begins with:

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE collaborationauthorlist SYSTEM "author.dtd">
```

## 📑 Input Format (CSV)

The CSV file must include at least these columns:

- `Surname`
- `Initials`
- `Given Name`
- `Institution`
- `Institution Code`
- `ORCID`

Each author may have multiple institutions (separated by commas in the `Institution Code` field). Institution names may contain `{}` brackets to extract formal names.

## 📚 References & Standards

Based on INSPIRE guidelines:
> https://github.com/inspirehep/author.xml

This project ensures that:
- Author metadata is properly associated with institutions.
- ORCID identifiers and collaboration info are embedded.
- Submission records are ready for downstream processing.

## 👤 Author

**Zane Gerber**  
zane.gerber@utah.edu

import re
import spacy

# Load spaCy model globally so it can be reused across multiple function calls
nlp = spacy.load("en_core_web_sm")

def nlp_parser(reference_string):
    """
    Parses multiple reference strings separated by newlines to extract authors, year, title, journal, volume, issue, pages, DOI, editors, and institution.

    Args:
        reference_string (str): The reference string or multiple reference strings separated by newlines.

    Returns:
        list: A list of dictionaries, each containing parsed fields for a reference.
    """
    # Split the input string by newlines and remove any empty lines
    references = [ref.strip() for ref in reference_string.split('\n') if ref.strip()]

    parsed_references = []

    for reference in references:
        # Regex for DOI extraction
        doi_pattern = r'(https?://doi\.org/[^\s]+)'
        doi_match = re.search(doi_pattern, reference)
        doi = doi_match.group(0) if doi_match else ''

        # Initialize a dictionary to store parsed data
        parsed_reference = {
            'doi': doi,
            'authors': '',
            'year': '',
            'title': '',
            'journal': '',
            'volume': '',
            'issue': '',
            'pages': '',
            'editors': '',
            'institution': '',
            'type': '',
            "original_string": reference
        }

        # Step 1: Extract authors using custom regex pattern
        # Pattern for authors (matches Last name followed by initials, possibly with multiple authors separated by commas)
        author_pattern = r'([A-Za-z\-]+(?:, [A-Z]\. ?)+|& [A-Za-z\-]+(?:, [A-Z]\. ?)+)'
        author_matches = re.findall(author_pattern, reference)

        if author_matches:
            # Clean up authors list and remove any trailing commas or spaces
            cleaned_authors = [author.strip() for author in author_matches]
            parsed_reference['authors'] = ', '.join(cleaned_authors)

        # Process the reference with spaCy for Named Entity Recognition to extract other details
        doc = nlp(reference)

        # Step 2: Extract year using regex
        year_pattern = r'\(\d{4}[a-z]?\)'  # Matches (2009a), (2009), etc.
        year_match = re.search(year_pattern, reference)
        if year_match:
            parsed_reference['year'] = year_match.group(0).strip('()')

        # Step 3: Extract title using position heuristics (between year and journal/institution)
        if year_match:
            year_end = year_match.end()
            institution_match = re.search(r'(University|Institute|Laboratory|Technology|School of [^\s]+)', reference, re.IGNORECASE)
            journal_match = re.search(r'([A-Za-z\s]+),? \d{1,2}\(', reference)  # Simple pattern for journal detection

            # Use heuristics to extract title
            if institution_match:
                inst_start = institution_match.start()
                parsed_reference['title'] = reference[year_end:inst_start].strip('. ')
            elif journal_match:
                journal_start = journal_match.start()
                parsed_reference['title'] = reference[year_end:journal_start].strip('. ')
            else:
                # General heuristic to find anything after the year if no match
                parsed_reference['title'] = reference[year_end:].split('.')[0].strip()

        # Step 4: Extract journal, volume, issue, and pages using regex
        volume_issue_pages_pattern = r'(\d+)\((\d+)\),\s*(\d+–\d+|\d+)'
        volume_issue_pages_match = re.search(volume_issue_pages_pattern, reference)

        if volume_issue_pages_match:
            parsed_reference['volume'] = volume_issue_pages_match.group(1)
            parsed_reference['issue'] = volume_issue_pages_match.group(2)
            parsed_reference['pages'] = volume_issue_pages_match.group(3)

        # Step 5: Extract type of publication and institution
        type_pattern = r'\b(Technical report|Working paper|Thesis|Dissertation)\b'
        type_match = re.search(type_pattern, reference, re.IGNORECASE)
        if type_match:
            parsed_reference['type'] = type_match.group(0)

        # Extract institution (if present)
        if institution_match:
            parsed_reference['institution'] = institution_match.group(0)

        # Append parsed reference to the list
        parsed_references.append(parsed_reference)

    # Return the list of parsed references
    return parsed_references


# # Example usage:
# reference_string = """
# Tang, K., Li, X., Suganthan, P. N., Yang, Z., & Weise, T. (Eds.). (2009a). Benchmark functions for the CEC'2008 special session and competition on large scale global optimization. Technical report (p. 1). University of Science and Technology of China.
# Tang, X., P. N., T. (2010). Some title. Journal of Testing, 1(1), 1-10.
# """

# # Print the parsed references
# print(nlp_parser(reference_string))

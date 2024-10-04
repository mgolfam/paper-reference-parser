import re

class ReferenceParser:
    
    def __init__(self, reference_string):
        self.reference_string = reference_string.strip()
        self.parsed_reference = self.parse_reference()

    def parse_reference(self):
        # Step 1: Extract year
        year_match = re.search(r'\((\d{4}[a-z]?)\)', self.reference_string)
        year = year_match.group(1) if year_match else " "

        # Step 2: Extract author(s) - assuming authors are at the start until the first period
        author_part = self.reference_string.split(".")[0].strip()

        # Step 3: Extract title - assuming title is between the first period and the journal
        remaining_text = self.reference_string.split(".", 1)[1].strip() if '.' in self.reference_string else ""
        title_match = re.search(r'(.+?)\. (.+)', remaining_text)
        title = title_match.group(1).strip() if title_match else " "

        # Step 4: Extract journal, volume, issue, and pages
        journal_match = re.search(r'(.+?), (\d+)\((\d+)\), (\d+–\d+)', remaining_text)
        if journal_match:
            journal = journal_match.group(1).strip()
            volume = journal_match.group(2).strip()
            issue = journal_match.group(3).strip()
            pages = journal_match.group(4).strip()
        else:
            journal, volume, issue, pages = " ", " ", " ", " "

        # Step 5: Extract DOI or URL if available
        doi_match = re.search(r'(https?://[^\s]+)', self.reference_string)
        doi = doi_match.group(1) if doi_match else " "

        # Return parsed reference as a dictionary
        return {
            "author": author_part,
            "year": year,
            "title": title,
            "journal": journal,
            "volume": volume,
            "issue": issue,
            "pages": pages,
            "doi": doi
        }

    def get_parsed_reference(self):
        return self.parsed_reference

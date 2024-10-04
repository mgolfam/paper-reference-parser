import re

class ReferenceParser:
    
    def __init__(self, reference_string):
        self.reference_string = reference_string.strip()
        self.regex_patterns = self.define_regex_patterns()
        self.parsed_reference = self.parse_reference()

    def define_regex_patterns(self):
        """
        Define multiple regex patterns for parsing different reference formats.
        """
        patterns = [
            # Pattern 1: General format (authors, year, title, journal, volume(issue), pages)
            r'(?P<authors>.+?) \((?P<year>\d{4}[a-z]?)\)\. (?P<title>.+?)\. (?P<journal>.+?), (?P<volume>\d+)\((?P<issue>\d+)\), (?P<pages>\d+–?\d*)\.?(?P<doi>https?://[^\s]+)?',
            
            # Pattern 2: Format without issue number
            r'(?P<authors>.+?) \((?P<year>\d{4}[a-z]?)\)\. (?P<title>.+?)\. (?P<journal>.+?), (?P<volume>\d+), (?P<pages>\d+–?\d*)\.?(?P<doi>https?://[^\s]+)?',
            
            # Pattern 3: Conference or book format
            r'(?P<authors>.+?) \((?P<year>\d{4}[a-z]?)\)\. (?P<title>.+?)\. In: (?P<editor>.+?), (?P<book_title>.+?), (?P<pages>\d+–?\d*)\.?(?P<doi>https?://[^\s]+)?',

            # Pattern 4: Technical report format
            r'(?P<authors>.+?) \((?P<year>\d{4}[a-z]?)\)\. (?P<title>.+?)\. (?P<report>.+?)\. (?P<institution>.+?)\.?(?P<doi>https?://[^\s]+)?'
        ]
        return patterns

    def apply_regex_patterns(self):
        """
        Apply each regex pattern to the reference string and return the best match.
        """
        best_match = None
        max_score = 0

        for pattern in self.regex_patterns:
            match = re.search(pattern, self.reference_string)
            if match:
                # Evaluate how many fields were matched
                score = len([group for group in match.groupdict().values() if group is not None])
                if score > max_score:
                    max_score = score
                    best_match = match

        return best_match

    def parse_reference(self):
        """
        Parse the reference string by trying multiple regex patterns and choosing the best one.
        """
        match = self.apply_regex_patterns()
        if match:
            parsed_reference = match.groupdict()
            # Fill missing fields with a blank space
            for field in ['authors', 'year', 'title', 'journal', 'volume', 'issue', 'pages', 'doi', 'book_title', 'editor', 'report', 'institution']:
                if field not in parsed_reference or parsed_reference[field] is None:
                    parsed_reference[field] = ' '  # Fill missing fields with a blank space
            return parsed_reference
        else:
            return {
                'authors': ' ',
                'year': ' ',
                'title': ' ',
                'journal': ' ',
                'volume': ' ',
                'issue': ' ',
                'pages': ' ',
                'doi': ' ',
                'book_title': ' ',
                'editor': ' ',
                'report': ' ',
                'institution': ' '
            }

    def get_parsed_reference(self):
        return self.parsed_reference

class BruteForceReferenceParser:
    
    def __init__(self, reference_string):
        # Split the input string by newline characters and strip extra whitespace
        self.reference_strings = [ref.strip() for ref in reference_string.split('\n') if ref.strip()]
        self.regex_patterns = self.define_regex_patterns()
        self.parsed_references = self.parse_multiple_references()

    def define_regex_patterns(self):
        """
        Define multiple regex patterns for parsing different reference formats.
        """
        patterns = [
            # Journal article format with DOI, handling multiline input
            r'(?P<authors>.+?) \((?P<year>\d{4}[a-z]?)\)\. (?P<title>.+?)\. (?P<journal>.+?), (?P<volume>\d+)\((?P<issue>\d+)\), (?P<pages>\d+–?\d*)\. (?P<doi>https?://[^\s]+)',
            
            # Journal article format without DOI, handling multiline input
            r'(?P<authors>.+?) \((?P<year>\d{4}[a-z]?)\)\. (?P<title>.+?)\. (?P<journal>.+?), (?P<volume>\d+)\((?P<issue>\d+)\), (?P<pages>\d+–?\d*)',
            
            # Conference paper or book chapter format, handling multiline input
            r'(?P<authors>.+?) \((?P<year>\d{4}[a-z]?)\)\. (?P<title>.+?)\. In: (?P<editor>.+?), (?P<book_title>.+?), pp\. (?P<pages>\d+–?\d*)\. (?P<doi>https?://[^\s]+)?',

            # Technical report or book format, handling multiline input
            r'(?P<authors>.+?) \((?P<year>\d{4}[a-z]?)\)\. (?P<title>.+?)\. (?P<report>.+?)\. (?P<institution>.+?)\. (?P<doi>https?://[^\s]+)?'
        ]
        return patterns

    def apply_regex_patterns(self, reference_string):
        """
        Apply each regex pattern to the reference string and return the best match.
        """
        best_match = None
        max_score = 0

        for pattern in self.regex_patterns:
            match = re.search(pattern, reference_string, re.DOTALL)
            if match:
                # Evaluate how many fields were matched
                score = len([group for group in match.groupdict().values() if group is not None])
                if score > max_score:
                    max_score = score
                    best_match = match

        return best_match

    def parse_reference(self, reference_string):
        """
        Parse a single reference string by trying multiple regex patterns and choosing the best one.
        """
        match = self.apply_regex_patterns(reference_string)
        if match:
            parsed_reference = match.groupdict()
            # Fill missing fields with a blank space
            for field in ['authors', 'year', 'title', 'journal', 'volume', 'issue', 'pages', 'doi', 'book_title', 'editor', 'report', 'institution']:
                if field not in parsed_reference or parsed_reference[field] is None:
                    parsed_reference[field] = ' '  # Fill missing fields with a blank space
            return parsed_reference
        else:
            return {
                'authors': ' ',
                'year': ' ',
                'title': ' ',
                'journal': ' ',
                'volume': ' ',
                'issue': ' ',
                'pages': ' ',
                'doi': ' ',
                'book_title': ' ',
                'editor': ' ',
                'report': ' ',
                'institution': ' '
            }

    def parse_multiple_references(self):
        """
        Parse multiple references (split by newline) and return a list of parsed references.
        """
        parsed_references = []
        for reference_string in self.reference_strings:
            parsed_reference = self.parse_reference(reference_string)
            parsed_references.append(parsed_reference)
        return parsed_references

    def get_parsed_references(self):
        return self.parsed_references
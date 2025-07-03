# AspPy2: Simple API for modeling ASP programs as lines of strings

class Line:
    """
    Represents a single line of ASP code, with optional metadata (e.g., CNL/NL mapping).
    """
    def __init__(self, asp_code, cnl_map=None):
        self.asp_code = asp_code  # The ASP rule/fact/constraint as a string
        self.cnl_map = cnl_map or {}  # Optional: mapping for explanations/variations

    def __str__(self):
        return self.asp_code

class ASPProgram:
    """
    Stores an ASP program as a list of Line objects.
    """
    def __init__(self):
        self.lines = []  # List of Line objects

    def add_line(self, asp_code, cnl_map=None):
        """
        Add a line of ASP code (as a string) to the program.
        Optionally, attach a CNL/NL mapping.
        """
        self.lines.append(Line(asp_code, cnl_map))

    def __str__(self):
        """
        Render the ASP program as a string (just the ASP code).
        """
        return "\n".join(str(line) for line in self.lines)

    def get_lines(self):
        """
        Return the list of Line objects.
        """
        return self.lines
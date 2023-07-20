import re


class PDF_wrapper:
    def __init__(self, file_name : str):
        self.file_name = file_name
        self.recipient = None
        self.origin = None
        self.reference = None
        self.identification = None
        self.date = None

        file_name = file_name.strip(".pdf")
        parts = file_name.split(" - ")

        try:
            if len(parts) < 5:
                raise ValueError(f"Invalid filename {file_name}. Check the format.")
            # The first part is the recipient
            self.recipient = parts[0]

            # The second part is the origin
            self.origin = parts[1]

            # The third part is the reference
            self.reference = parts[2]

            # The last part is the date. We check it with a simple regex to confirm.
            date_pattern = re.compile("\d{2}.\d{2}.\d{4}$")
            if date_pattern.match(parts[-1]):
                self.date = parts[-1]
            else:
                raise ValueError(f"Invalid date in filename {file_name}. Check the format.")

            # Everything else is part of the identification
            self.identification = " - ".join(parts[3:-1])
        except ValueError: pass

    def to_dict(self):
        return {
            "file_name": self.file_name,
            "recipient": self.recipient,
            "origin": self.origin,
            "reference": self.reference,
            "identification": self.identification,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, data: dict):
        pdf = cls(data["file_name"])
        pdf.recipient = data.get("recipient")
        pdf.origin = data.get("origin")
        pdf.reference = data.get("reference")
        pdf.identification = data.get("identification")
        pdf.date = data.get("date")
        return pdf

    def parse_metadata(self, metadata: str):
        # Assuming the metadata is a string separated by hyphens
        # like this: "recipient - origin - reference - identification - date"
        parts = metadata.split(" - ")

        if len(parts) == 5:
            self.recipient, self.origin, self.reference, self.identification, self.date = parts
        else:
            print("Invalid metadata string. Please check the format.")


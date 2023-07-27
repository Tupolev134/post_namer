import json


class Profile:
    def __init__(self, name=None, path=None, path_to_scans=None, path_to_this_profile=None):
        self.name = name
        self.path_to_root = path
        self.path_to_scans = path_to_scans
        self.path_to_this_profile = path_to_this_profile
        self.recipients = list()
        self.origins = list()
        self.references = list()
        self.identifications = list()

    def to_dict(self):
        return {
            "name": self.name,
            "path_to_root": self.path_to_root,
            "path_to_scans": self.path_to_scans,
            "path_to_this_profile": self.path_to_this_profile,
            "recipients": self.recipients,
            "origins": self.origins,
            "references": self.references,
            "identifications": self.identifications,
        }

    @classmethod
    def from_dict(cls, data: dict):
        profile = cls(data["name"], data["path_to_root"], data["path_to_scans"], data['path_to_this_profile'])
        profile.recipients = data.get("recipients", [])
        profile.origins = data.get("origins", [])
        profile.references = data.get("references", [])
        profile.identifications = data.get("identifications", [])
        return profile

    def save_to_json(self, filename: str):
        with open(filename, "w") as file:
            json.dump(self.to_dict(), file)

    @classmethod
    def load_from_json(cls, filename: str):
        with open(filename, "r") as file:
            data = json.load(file)
        return cls.from_dict(data)

    def add_recipient(self, recipient):
        for i, (rec, count) in enumerate(self.recipients):
            if rec == recipient:
                self.recipients[i] = (rec, count + 1)
                return
        self.recipients.append((recipient, 1))

    def add_origin(self, origin):
        for i, (org, count) in enumerate(self.origins):
            if org == origin:
                self.origins[i] = (org, count + 1)
                return
        self.origins.append((origin, 1))

    def add_reference(self, reference):
        for i, (ref, count) in enumerate(self.references):
            if ref == reference:
                self.references[i] = (ref, count + 1)
                return
        self.references.append((reference, 1))

    def add_identification(self, identification):
        for i, (iden, count) in enumerate(self.identifications):
            if iden == identification:
                self.identifications[i] = (iden, count + 1)
                return
        self.identifications.append((identification, 1))

import json

class EmailTemplate:
    def __init__(self, template_name=None):
        self.template_name = template_name
        self.sender = ""        # outgoing email address
        self.to = list()        # list of recipients mail addresses
        self.cc = list()        # list of cc recipients mail addresses
        self.bcc = list()       # list of bcc recipients mail addresses
        self.subject = ""     # subject of the mail template
        self.body = ""        # body of the mail template
        self.attachments = "" # list of paths to files

    def to_dict(self):
        return {
            'template_name': self.template_name,
            'sender': self.sender,
            'to': self.to,
            'cc': self.cc,
            'bcc': self.bcc,
            'subject': self.subject,
            'body': self.body,
            'attachments': self.attachments,
        }

    @classmethod
    def from_dict(cls, data):
        template = EmailTemplate(data.get('template_name'))
        template.sender = data.get('sender')
        template.to = data.get('to', [])
        template.cc = data.get('cc', [])
        template.bcc = data.get('bcc', [])
        template.subject = data.get('subject')
        template.body = data.get('body')
        template.attachments = data.get('attachments', [])
        return template

    def save_to_json(self, file_path):
        with open(file_path, 'w') as file:
            json.dump(self.to_dict(), file)

    @classmethod
    def load_from_json(cls, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return cls.from_dict(data)

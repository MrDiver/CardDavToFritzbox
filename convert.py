import os

class VCard:
    def __init__(self):
        self.email: str = ""
        self.name: str = ""
        self.tel: str = ""
        self.uid: str = ""

    def tofritz(self):
        return f"""
        <contact>
            <category>0</category>
            <person>
                <realName>{self.name}</realName>
            </person>
            <telephony nid="1">
                <number type="mobile" prio="0" id="0">{self.tel}</number>
            </telephony>
            <services nid="1">
                <email classifier="private" id="0">{self.email}</email>
            </services>
            <setup/>
            <features doorphone="0"/>
            <mod_time>0</mod_time>
            <uniqueid>{self.uid}</uniqueid>
        </contact>
        """

    def __repr__(self):
        return f"""=== VCard ===
uid: \t{self.uid}
Name: \t{self.name}
Email: \t{self.email}
Tel: \t{self.tel}
        """


def parse_vcard(document):
    vcard = VCard()
    for line in document:
        line: str
        if line.startswith("EMAIL"):
            pos = line.find("work:") + 5
            vcard.email = line[pos:].strip()
        if line.startswith("N:"):
            tmp = line[2:]
            pos = tmp.find(";")
            vorname = tmp[pos+1:].strip()
            nachname = tmp[:pos].strip()
            vcard.name = f"[FS] {vorname} {nachname}"
        if line.startswith("UID:"):
            vcard.uid = line[4:].strip()
        if line.startswith("TEL"):
            pos = line.find(":") + 1
            vcard.tel = line[pos:].strip()
    return vcard

contacts = []
for filename in os.listdir("carddav"):
    with open(f"carddav/{filename}") as content:
        vcard = parse_vcard(content.readlines())
        contacts.append(vcard)

xml_contacts = "".join([c.tofritz() for c in contacts])

export = f"""
<phonebooks>
    <phonebook name="LDAP">
    {xml_contacts}
    </phonebook>
</phonebooks>
"""

print(export)

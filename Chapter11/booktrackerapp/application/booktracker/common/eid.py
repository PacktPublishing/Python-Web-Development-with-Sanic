import uuid
from string import ascii_letters, digits

REQUEST_ID_ALPHABET = ascii_letters + digits
REQUEST_ID_ALPHABET_LENGTH = len(REQUEST_ID_ALPHABET)


def generate(width: int = 0, fillchar: str = "x"):
    """
    Generate a UUID and make is smaller
    """
    output = ""
    uid = uuid.uuid4()
    num = uid.int
    while num:
        num, pos = divmod(num, REQUEST_ID_ALPHABET_LENGTH)
        output += REQUEST_ID_ALPHABET[pos]
    eid = output[::-1]
    if width:
        eid = eid.rjust(width, fillchar)
    return eid

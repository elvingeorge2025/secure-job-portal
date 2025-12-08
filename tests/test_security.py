from security.password_utils import hash_password, verify_password
from security.validators import allowed_file


def test_password_hashing():
    pwd = "SecurePass123"
    hashed = hash_password(pwd)
    assert verify_password(pwd, hashed)
    assert not verify_password("wrong", hashed)


def test_allowed_file():
    assert allowed_file("cv.pdf")
    assert not allowed_file("cv.exe")

import pytest


@pytest.mark.usefixtures("login")
class BaseTest:
    pass

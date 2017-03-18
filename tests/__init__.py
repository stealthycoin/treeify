import mock
from io import StringIO
from contextlib import contextmanager


@contextmanager
def consume_stdout():
    stdout = StringIO()
    with mock.patch('sys.stdout', stdout):
        yield stdout

import unittest
from tests import consume_stdout
from treeify import Treeify, BadNodeError
from treeify.adapters import DictAdapter, FnAdapter


class Branch(object):
    def __init__(self, value, children):
        self.children = children
        self.foo = value


class BadBranch(object):
    def __init__(self, value):
        self._children = []
        self.foo = value


class Leaf(object):
    def __init__(self, value):
        self.bar = value


class BadLeaf(object):
    def __init__(self):
        self._bar = None


class FnBranch(object):
    def __init__(self, value, children, real_children):
        self.foo = value
        self.children = children
        self.real_children = real_children


class TestTreeify(unittest.TestCase):
    def setUp(self):
        self.treeify = Treeify('children', 'foo', 'bar', prefix='  ',
                               right_prefix='  ')

    def test_empty(self):
        with self.assertRaises(BadNodeError):
            list(self.treeify.traverse(None))

    def test_invalid_leaf_key(self):
        root = BadLeaf()
        with self.assertRaises(BadNodeError):
            list(self.treeify.traverse(root))

    def test_branch_children(self):
        root = BadBranch('foo')
        with self.assertRaises(BadNodeError):
            list(self.treeify.traverse(root))

    def test_basic_case(self):
        root = Branch('foo', [Leaf('bar'), Leaf('baz')])
        self.assertEqual(list(self.treeify.traverse(root)),
                         ['foo', '  bar', '  baz'])

    def test_nested_case(self):
        root = Branch('foo', [Branch('bar', [Leaf('quux'), Leaf('xyzzy')]),
                              Branch('baz', [Leaf('qux')])])
        self.assertEqual(list(self.treeify.traverse(root)),
                         ['foo', '  bar', '    quux', '    xyzzy', '  baz',
                          '    qux'])

    def test_child_adapter_dict(self):
        self.treeify._child_adapter = DictAdapter('real_children')
        root = FnBranch('foo', ['bar', 'baz'], {'bar': Leaf('qux'),
                                                'baz': Leaf('quxx')})
        self.assertEqual(list(self.treeify.traverse(root)),
                         ['foo', '  qux', '  quxx'])

    def test_child_adapter_callable(self):
        def inner(key):
            if key == 'bar':
                return Leaf('qux')
            elif key == 'baz':
                return Leaf('quxx')

        self.treeify._child_adapter = FnAdapter('real_children')
        root = FnBranch('foo', ['bar', 'baz'], inner)
        self.assertEqual(list(self.treeify.traverse(root)),
                         ['foo', '  qux', '  quxx'])

    def test_string_output(self):
        root = Branch('foo', [Leaf('bar'), Leaf('baz')])
        with consume_stdout() as output:
            self.treeify.show_traverse(root)
        self.assertEqual("foo\n  bar\n  baz\n", output.getvalue())

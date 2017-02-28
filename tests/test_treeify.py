import unittest
from treeify.treeify import Treeify, BadNodeError


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


class TestTreeify(unittest.TestCase):
    def setUp(self):
        self.treeify = Treeify('children', 'foo', 'bar')

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
        root = Branch('foo', [Branch('bar', [Leaf('xyzzy')]),
                              Branch('baz', [Leaf('qux')])])
        self.treeify.show_traverse(root)

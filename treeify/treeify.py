import sys


T_BRACKET = u'\u251C'
HORIZ_BAR = u'\u2500'
VERT_BAR = u'\u2502'
DEFAULT_PREFIX = VERT_BAR + u'  '
RIGHTMOST_PREFIX = T_BRACKET + HORIZ_BAR + HORIZ_BAR


class BadNodeError(RuntimeError):
    pass


class Treeify(object):
    def __init__(self, children_key, branch_str_key, leaf_str_key,
                 prefix=DEFAULT_PREFIX, right_prefix=RIGHTMOST_PREFIX,
                 child_adapter=None):
        self._children_key = children_key
        self._branch_str_key = branch_str_key
        self._leaf_str_key = leaf_str_key
        self._prefix = prefix
        self._right_prefix = right_prefix
        self._child_adapter = child_adapter

    def _traverse(self, obj, depth):
        has_valid_child_fn = False
        if self._child_adapter:
            has_valid_child_fn = self._child_adapter.can_use_adapter(self)
        has_children_key = hasattr(obj,
                                   self._children_key) or has_valid_child_fn
        has_branch_str_key = hasattr(obj, self._branch_str_key)
        has_leaf_string_key = hasattr(obj, self._leaf_str_key)

        prefix = self._prefix * (depth - 1)
        if depth >= 1:
            prefix += self._right_prefix

        if has_children_key and has_branch_str_key:
            # Branch node, yield name and recurse.
            children = getattr(obj, self._children_key)
            value = getattr(obj, self._branch_str_key)
            yield '%s%s' % (prefix, value)
            for child in children:
                if self._child_adapter:
                    child = self._child_adapter.adapt(obj, child)
                for msg in self._traverse(child, depth + 1):
                    yield msg

        elif has_leaf_string_key:
            # Leaf node, yield name.
            value = getattr(obj, self._leaf_str_key)
            yield '%s%s' % (prefix, value)
        else:
            raise BadNodeError('%s does not have required keys needs either '
                               'both of [%s, %s] for a branch node or "%s" '
                               'for a leaf node.' % (obj,
                                                     self._children_key,
                                                     self._branch_str_key,
                                                     self._leaf_str_key))

    def traverse(self, obj):
        for msg in self._traverse(obj, 0):
            yield msg

    def show_traverse(self, obj):
        for msg in self.traverse(obj):
            sys.stdout.write('%s\n' % msg)

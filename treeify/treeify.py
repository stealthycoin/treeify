import sys


class BadNodeError(RuntimeError):
    pass


class Treeify(object):
    def __init__(self, children_key, branch_str_key, leaf_str_key,
                 prefix='  '):
        self._children_key = children_key
        self._branch_str_key = branch_str_key
        self._leaf_str_key = leaf_str_key
        self._prefix = prefix

    def _traverse(self, obj, depth):
        has_children_key = hasattr(obj, self._children_key)
        has_branch_str_key = hasattr(obj, self._branch_str_key)
        has_leaf_string_key = hasattr(obj, self._leaf_str_key)

        if has_children_key and has_branch_str_key:
            children = getattr(obj, self._children_key)
            value = getattr(obj, self._branch_str_key)
            yield '%s%s' % ((self._prefix * depth), value)
            for child in children:
                for msg in self._traverse(child, depth + 1):
                    yield msg

        elif has_leaf_string_key:
            value = getattr(obj, self._leaf_str_key)
            yield '%s%s' % ((self._prefix * depth), value)
        else:
            raise BadNodeError('%s does not have required keys needs either '
                               'both of [%s, %s] for a branch node or "%s" '
                               'for a leaf node.'% (obj,
                                                    self._children_key,
                                                    self._branch_str_key,
                                                    self._leaf_str_key))

    def traverse(self, obj):
        for msg in self._traverse(obj, 0):
            yield msg

    def show_traverse(self, obj):
        for msg in self.traverse(obj):
            sys.stdout.write('%s\n' % msg)

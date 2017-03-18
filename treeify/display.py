class Renderer(object):
    """Draws recursive structures similar to the 'tree' unix utility."""
    T_BRACKET = u'\u251C'
    HORIZ_BAR = u'\u2500'
    VERT_BAR = u'\u2502'
    DEFAULT_PREFIX = VERT_BAR + u'  '
    RIGHTMOST_PREFIX = T_BRACKET + HORIZ_BAR + HORIZ_BAR

    def get_prefix(self, depth):
        prefix = self.DEFAULT_PREFIX * (depth - 1)
        if depth >= 1:
            prefix += self.RIGHTMOST_PREFIX
        return prefix


class TestRenderer(Renderer):
    """Renderer used in tests for simplicity"""
    DEFAULT_PREFIX = '  '
    RIGHTMOST_PREFIX = '  '

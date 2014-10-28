# -*- coding:utf-8 -*-
#

#################################
# Directives                    #
#################################

from docutils.parsers.rst import directives
from . import BetterFigure


class XetexFigure(BetterFigure):
    only_target_tags = ['latex', 'tex', 'xelatex', 'xetex']

directives.register_directive('figure', XetexFigure)



#################################
# Writer                        #
#################################

from email.utils import parseaddr

from docutils.nodes import SkipNode, section
from docutils.writers.xetex import XeLaTeXTranslator
from docutils.writers.xetex import Writer as XeTexWriter
from docutils.writers.latex2e import PreambleCmds
from docutils.writers.latex2e import Table

class Writer(XeTexWriter):
    def __init__(self):
        XeTexWriter.__init__(self)
        self.translator_class = TECXeTexTranslator

class BetterTable(Table):
    # horizontal lines are drawn below a row,
    def get_opening(self,node):
        result = ['\n'.join([r'\setlength{\DUtablewidth}{\linewidth}',
                          r'\begin{%s}[c]' % self.get_latex_type()])]
        result.append('{%s}\n' % self.get_colspecs())
        #self.set('preamble written',1)
        result.append(r'\caption{%s}' '\n' % ''.join(self.caption))
        # Insert hyperlabel after (long)table, as
        # other places (beginning, caption) result in LaTeX errors.
        if node.get('ids'):
            result += self.ids_to_labels(node, set_anchor=False)
        result += "\\\\ \n"
        return result  
    def ids_to_labels(self, node, set_anchor=True):
        """Return list of label definitions for all ids of `node`

        If `set_anchor` is True, an anchor is set with \phantomsection.
        """
        labels = ['\\label{%s}' % id for id in node.get('ids', [])]
        if set_anchor and labels:
            labels.insert(0, '\\phantomsection')
        return labels
    def get_closing(self):
        closing = []
        if self._table_style == 'booktabs':
            closing.append(r'\bottomrule')
        # elif self._table_style == 'standard':
        #     closing.append(r'\hline')
        return '\n'.join(closing)
    def get_caption(self):
        if not self.caption:
            return ''
        caption = ''.join(self.caption)
        if 1 == self._translator.thead_depth():
            return r'\caption{%s}\\' '\n' % caption
        return r'\caption[]{%s (... continuaci\'on)}\\' '\n' % caption

    def depart_thead(self):
        a = []
        #if self._table_style == 'standard':
        #    a.append('\\hline\n')
        if self._table_style == 'booktabs':
            a.append('\\midrule\n')
        if self._latex_type == 'longtable':
            if 1 == self._translator.thead_depth():
                a.append('\\endfirsthead\n')
            else:
                a.append('\\endhead\n')
                a.append(r'\multicolumn{%d}{c}' % len(self._col_specs) +
                         r'{\hfill ... contin\'ua en la siguiente p\'agina} \\')
                a.append('\n\\endfoot\n\\endlastfoot\n')
        # for longtable one could add firsthead, foot and lastfoot
        self._in_thead -= 1
        return a

class TECXeTexTranslator(XeLaTeXTranslator):

    def __init__(self, document):
        XeLaTeXTranslator.__init__(self, document)
        self.active_table = BetterTable(
            self, 'longtable', self.settings.table_style
        )

    def visit_figure(self, node):
        self.requirements['float_settings'] = PreambleCmds.float_settings
        # The 'align' attribute sets the "outer alignment",
        # for "inner alignment" use LaTeX default alignment (similar to HTML)
        alignment = node.attributes.get('align', 'center')
        if alignment != 'center':
            # The LaTeX "figure" environment always uses the full textwidth,
            # so "outer alignment" is ignored. Just write a comment.
            # TODO: use the wrapfigure environment?
            self.out.append('\\begin{figure} %% align = "%s"\n' % alignment)
        else:
            self.out.append('\\begin{figure}\n')

    def depart_figure(self, node):
        if node.get('ids'):
            self.out += self.ids_to_labels(node) + ['\n']
        self.out.append('\\end{figure}\n')

    def depart_image(self, node):
        pass
        #if node.get('ids'):
        #    self.out += ["asdasdasd"] + self.ids_to_labels(node) + ['\n']

    def depart_table(self, node):
        # wrap content in the right environment:
        content = self.out
        self.pop_output_collector()
        self.out.extend(['\n'] + self.active_table.get_opening(node))
        self.out += content
        self.out.append(self.active_table.get_closing() + '\n')
        self.out.append(r'\end{%s}' % self.active_table.get_latex_type())
        self.active_table.close()
        if len(self.table_stack)>0:
            self.active_table = self.table_stack.pop()
        else:
            self.active_table.set_table_style(self.settings.table_style)

    def visit_thead(self, node):
        self._thead_depth += 1
        if 1 == self.thead_depth():
            self.active_table.get_colspecs()
            self.active_table.set('preamble written',1)
        else:
            self.out.append(self.active_table.get_caption())
        self.out.extend(self.active_table.visit_thead())


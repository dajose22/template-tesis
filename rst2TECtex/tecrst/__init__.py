# -*- coding:utf-8 -*-

from docutils.nodes import Element
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives.images import *


class BetterFigure(Figure):
    def align(argument):
        return directives.choice(argument, Figure.align_h_values)

    def figwidth_value(argument):
        if argument.lower() == 'image':
            return 'image'
        else:
            return directives.length_or_percentage_or_unitless(argument, 'px')

    option_spec = Image.option_spec.copy()
    option_spec['figwidth'] = figwidth_value
    option_spec['figclass'] = directives.class_option
    option_spec['align'] = align
    has_content = True
    def run(self):
        figwidth = self.options.pop('figwidth', None)
        figclasses = self.options.pop('figclass', None)
        align = self.options.pop('align', None)
        name = self.options.get('name',None)
        (image_node,) = Image.run(self)
        if isinstance(image_node, nodes.system_message):
            return [image_node]
        figure_node = nodes.figure('', image_node)
        if figwidth == 'image':
            if PIL and self.state.document.settings.file_insertion_enabled:
                imagepath = urllib.url2pathname(image_node['uri'])
                try:
                    if isinstance(imagepath, str):
                        imagepath_str = imagepath
                    else:
                        imagepath_str = imagepath.encode(sys.getfilesystemencoding())
                    img = PIL.Image.open(imagepath_str)
                except (IOError, UnicodeEncodeError):
                    pass # TODO: warn?
                else:
                    self.state.document.settings.record_dependencies.add(
                        imagepath.replace('\\', '/'))
                    figure_node['width'] = img.size[0]
                    del img
        elif figwidth is not None:
            figure_node['width'] = figwidth
        if figclasses:
            figure_node['classes'] += figclasses
        if align:
            figure_node['align'] = align
        if name:
            figure_node['ids'] = [fully_normalize_name(name)]
        if self.content:
            node = nodes.Element()          # anonymous container for parsing
            self.state.nested_parse(self.content, self.content_offset, node)
            first_node = node[0]
            if isinstance(first_node, nodes.paragraph):
                caption = nodes.caption(first_node.rawsource, '',
                                        *first_node.children)
                caption.source = first_node.source
                caption.line = first_node.line
                figure_node += caption
            elif not (isinstance(first_node, nodes.comment)
                      and len(first_node) == 0):
                error = self.state_machine.reporter.error(
                      'Figure caption must be a paragraph or empty comment.',
                      nodes.literal_block(self.block_text, self.block_text),
                      line=self.lineno)
                return [figure_node, error]
            if len(node) > 1:
                figure_node += nodes.legend('', *node[1:])
        return [figure_node]

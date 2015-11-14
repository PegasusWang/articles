#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import io
import os
from pprint import pprint
from html2text import html2text
from extract import extract as et
from extract import extract_all as et_all
from markdown2 import markdown, markdown_path


def get_all_files(path):
    res = set()
    list_dirs = os.walk(path)
    for root, dirs, files in list_dirs:
        for f in files:
            res.add(os.path.join(root, f))
    return res


def remove_words(s):
    for key in ['<!--NEWSZW_HZH_END-->', '<!--NEWSZW_HZH_BEGIN-->',
                'http://www.jb51.net', 'www.jb51.net', 'jb51.net']:
        s = s.replace(key, '')
    return s


def parse_jb51(html):
    html = unicode(html)
    html = html.replace(r'\r', '')
    art_title = et('<h1>', '</h1>',
                   et('<div id="daohang">', '<div id="art_info">', html))
    art_brief = et('<div id="art_demo">', '</div>', html)
    art_content = et('<div id="art_content">', '<div id="art_xg">', html)
    art_tags = list(et_all('">', '</a>', et('<div class="tags">', '</div>', html)))
    art_related_list = et_all('<a href="', '"', et('id=relatedarticle', '</ul>', html))
    art_related_id_list = [i.rsplit('/', 1)[1].split('.')[0]
                           for i in art_related_list if i]

    if art_brief:
        art_content = html2markdown(art_brief + '\n' + art_content)
    else:
        art_brief = html2markdown(art_content[0:100])
        art_content = html2markdown(art_content)

    art_brief = remove_words(art_brief)
    art_content = remove_words(art_content)

    to_save = {'art_title': 'title',
               'art_brief': 'brief',
               'art_content': 'content',
               'art_tags': 'tag_list',
               'art_related_id_list': 'related_list'
               }

    d = {}
    for k, v in locals().items():
        if k in to_save:
            key = to_save[k]
            d[key] = v
    return d


def html2markdown(html):
    return html2text(html)


def markdown2html(md):
    """对于代码块\n\n```\n\n + codeblock + \n\n```\n\n"""
    return markdown(md, extras=["code-friendly", 'fenced-code-blocks'])


def all_to_txt(input_path, output_path):
    i = 0
    max_cnt = 10

    all_files = get_all_files(input_path)
    for each in all_files:
        i += 1
        if i > max_cnt:
            break
        with open(each, 'r') as f:
            html = f.read()
            data = parse_jb51(html)
            filename = os.path.join(output_path,
                           os.path.basename(each).rsplit('.', 1)[0] + '.txt')
            print(filename)

            if data.get('brief'):
                print len(data.get('brief'))
            with io.open(filename, 'w+', encoding='utf-8') as outfile:
                data = json.dumps(data, ensure_ascii=False, encoding='utf-8',
                                  indent=4)

                outfile.write(unicode(data))


def all_to_html(input_path, output_path):
    all_files = get_all_files(input_path)
    for each in all_files:
        if each.endswith('txt'):
            with io.open(each, 'r', encoding='utf-8') as f:
                d = json.load(f)
                md = d.get('content')
                filename = os.path.join(output_path,
                            os.path.basename(each).rsplit('.', 1)[0] + '.html')
                print(filename)
                with io.open(filename, 'w+', encoding='utf-8') as f:
                    f.write(markdown2html(md))


def test():
    content = open('72000.html', 'r').read()
    d = parse_jb51(content)
    for k, v in d.items():
        print k, v

    content = d.get('content')
    md = html2markdown(content)
    with open('t.md', 'w+') as f:
        f.write(md)
    html = markdown2html(md)
    with open('t.html', 'w+') as f:
        f.write(html)


if __name__ == '__main__':
    #test()
    #all_to_txt('/home/wnn/raw/jb51_html', '/home/wnn/raw/jb51_txt')
    all_to_html('/home/wnn/raw/jb51_txt', '/home/wnn/raw/jb51_txt')

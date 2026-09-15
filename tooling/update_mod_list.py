"""Render the README mod list from the AntHub client manifest, without network requests."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    project = json.loads((ROOT / 'anthub.json').read_text())
    pack = json.loads((ROOT / project['pack']['manifest']).read_text())
    rows = ['<table width="100%">', '<tr><th>Обязательные</th><th>Рекомендуемые / необязательные</th></tr>', '<tr>']
    mods = [c for c in pack['components'] if any(f['path'].startswith('mods/') for f in c['files'])]
    for required in (True, False):
        rows.append('<td width="50%" valign="top"><ul>')
        for c in sorted(mods, key=lambda c: c['name'].casefold()):
            if (c['kind'] == 'required') != required:
                continue
            f = next(f for f in c['files'] if f['path'].startswith('mods/'))
            label = html.escape(c['name'])
            url = html.escape(f['url'], quote=True)
            version = html.escape(f['version'])
            rows.append(f'<li><a href="{url}">{label}</a> [{version}]</li>')
        rows.append('</ul></td>')
    rows += ['</tr>', '</table>']
    start, end = '<div id="mod-list">', '<a name="mod-list-end"></a>'
    path = ROOT / 'README.md'
    text = path.read_text()
    if text.count(start) != 1 or text.count(end) != 1 or text.index(start) >= text.index(end):
        raise ValueError('Expected unique ordered mod-list markers')
    block = start + '\n\n<p>Состав сборки ' + html.escape(project['pack']['version']) + ' · источник: <code>pack/client.json</code>.</p>\n\n' + '\n'.join(rows) + '\n\n</div>\n\n'
    path.write_text(text[:text.index(start)] + block + text[text.index(end):])
    print(f'Rendered {len(mods)} mods')

if __name__ == '__main__':
    main()

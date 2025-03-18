#!/bin/python

import json
import subprocess
import zipfile
from pathlib import Path

subprocess.run(['../packwiz', 'modrinth', 'export', '-o', '../Elysium-packwiz.mrpack', '-y'], cwd=Path('./src'), check=True)

with (zipfile.ZipFile('Elysium-packwiz.mrpack', 'r') as src, zipfile.ZipFile('Elysium.mrpack', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as dst):
    for info in src.infolist():
        with src.open(info) as file:
            if info.filename == "modrinth.index.json":
                content = json.loads(file.read())
                for modfile in content['files']:
                    if 'env' in modfile and \
                            modfile['env']['client'] == 'unsupported' and \
                            modfile['env']['server'] == 'required':
                        modfile['env']['client'] = 'required'
                dst.writestr(info.filename, json.dumps(content, ensure_ascii=False))
            else:
                dst.writestr(info.filename, file.read())

import re
import glob
import sys

#Mise en place de la nouvelle terminologie segmOnto dans les labels 
Zone = {
    "Main": "MainZone",
    "Default": "MainZone",
    "MainZone": "MainZone",
    "DropCapital": "DropCapitalZone",
    "RunningTitle": "RunningTitleZone",
    "Margin": "MarginTextZone",
    "Numbering": "NumberingZone",
    "Signatures" : "QuireMarksZone",
    "Damage" : "DamageZone",
    "Decoration" : "GraphicZone",
    "Figure" : "GraphicZone",
    "MusicNotation" : "MusicZone",
    "Seal" : "SealZone",
    "Stamp" : "StampZone",
    "Table" : "TableZone",
    "Title" : "TitlePageZone",
    'DropCapitalLine' : "DropCapitalZone",
}
Line = {
    'Rubric': "HeadingLine",
    'Default': "DefaultLine",
    'Main': "DefaultLine",
    'DropCapital' : "DropCapitalLine",
    'DropCapitalLine' : "DropCapitalLine",
    'MusicLine' : "MusicLine",
    'Numbering' : "DefaultLine",
    'Interlinear' : "InterlinearLine"
}
regex = re.compile(r'LABEL="(\w+)"(\s+)DESCRIPTION="([ \w]+)"')


def replace(match):
    label, space, desc = match.groups()
    if desc.startswith("block type"):
        if desc.endswith("Zone"):
            print(f"Ignoring {label}")
            return f"""LABEL="{label}"{space}DESCRIPTION="{desc}\""""
        desc = f"block type {Zone[label]}"
        label = Zone[label]
        #data.append(label)
    else:
        if desc.endswith("Line"):
            print(f"Ignoring {label}")
            return f"""LABEL="{label}"{space}DESCRIPTION="{desc}\""""
        desc = f"line type {Line[label]}"
        label = Line[label]
    return f"""LABEL="{label}"{space}DESCRIPTION="{desc}\""""

for file in sys.argv[1:]:
    with open(file) as f:
        xml = f.read()

    xml = regex.sub(replace, xml)
    with open(file, "w") as f:
        f.write(xml)
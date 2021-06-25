from typing import Iterable, Optional

import lxml.etree as ET
import click
import tqdm


@click.command()
@click.option("-s", "--suffix", default=None, help="If set, adds a suffix, otherwise, replace the current file",
              show_default=True)
@click.argument("xsl_path", type=click.Path(exists=True, file_okay=True, dir_okay=False), nargs=1)
@click.argument("files", type=click.Path(exists=True, file_okay=True, dir_okay=False), nargs=-1)
def run(xsl_path: str, files: Iterable[str], suffix: Optional[str] = None):
    """ Applies XSLT at [XSL_PATH] on [FILES]"""
    xsl = ET.XSLT(ET.parse(xsl_path))

    for file_path in tqdm.tqdm(files):
        xml = ET.parse(file_path)
        new_xml = xsl(xml)
        new_file = file_path
        if suffix:
            new_file = new_file.replace(".xml", suffix)
        with open(new_file, "w") as out:
            out.write(str(new_xml))


if __name__ == "__main__":
    run()

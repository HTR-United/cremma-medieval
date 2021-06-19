import os
import sys
import click
from lxml import etree


class Validator:
    def __init__(self, xsd_path: str):
        xmlschema_doc = etree.parse(xsd_path)
        self.xmlschema = etree.XMLSchema(xmlschema_doc)

    def validate(self, xml_path: str) -> bool:
        xml_doc = etree.parse(xml_path)
        result = self.xmlschema.validate(xml_doc)

        return result


@click.command()
@click.argument("xsd")
@click.argument("files", nargs=-1)
@click.option("-v", "--verbose", default=False, is_flag=True)
def test(xsd, files, verbose: bool = False):
    validator = Validator(xsd)
    failed = False
    errors = []
    for file_name in files:
        if validator.validate(file_name):
            click.echo(f"Testing {file_name}: Valid")
            errors.append(0)
        else:
            failed = True
            click.echo(click.style(f"Testing {file_name}: Invalid", fg="red"))
            if verbose:
                click.echo(click.style(
                    str(validator.xmlschema.error_log).replace(f"{file_name}:", "").replace("{http://www.loc.gov/standards/alto/ns-v4#}", "alto:"),
                    fg="yellow")
                )
            errors.append(1)

    click.echo("\n\n\n=====\nREPORT\n=====\n")
    click.echo(f"{sum(errors)}/{len(errors)} invalid XML files")
    if failed:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    test()
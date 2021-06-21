from typing import Iterable
import sys
import click
from lxml import etree
from collections import defaultdict


class Validator:
    def __init__(self, xsd_path: str):
        xmlschema_doc = etree.parse(xsd_path)
        self.xmlschema = etree.XMLSchema(xmlschema_doc)

    def validate(self, xml_path: str) -> bool:
        xml_doc = etree.parse(xml_path)
        result = self.xmlschema.validate(xml_doc)

        return result


def simplify_log_line(string: etree._LogEntry) -> str:
    return string.message.replace("{http://www.loc.gov/standards/alto/ns-v4#}", "alto:")


def print_error_log(error_log: Iterable[etree._LogEntry], group: bool = False) -> None:
    errors = defaultdict(list)
    for line in error_log:
        if group:
            errors[simplify_log_line(line)].append(str(line.line))
        else:
            click.secho(
                f"\tLine {line.line:04d}: {simplify_log_line(line)}",
                fg="yellow",
                color=True
            )

    for error, lines in errors.items():
        click.secho(
            f"\t{error} on line(s): {', '.join(lines)}",
            fg="yellow",
            color=True
        )

@click.command()
@click.argument("xsd")
@click.argument("files", nargs=-1)
@click.option("-v", "--verbose", default=False, is_flag=True)
@click.option("-g", "--group", default=False, is_flag=True, help="Group error types")
def test(xsd, files, verbose: bool = False, group: bool = False):
    validator = Validator(xsd)
    failed = False
    errors = []
    for file_name in files:
        if validator.validate(file_name):
            click.echo(f"Testing {file_name}: Valid")
            errors.append(0)
        else:
            failed = True
            click.echo(click.style(f"Testing {file_name}: Invalid", fg="red"), color=True)
            if verbose:
                print_error_log(validator.xmlschema.error_log, group=group)
            errors.append(1)

    click.echo("\n\n\n=====\nREPORT\n=====\n")
    click.echo(f"{sum(errors)}/{len(errors)} invalid XML files")
    if failed:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    test()
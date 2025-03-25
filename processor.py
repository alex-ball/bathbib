#!/usr/bin/env python3
from dataclasses import dataclass, field
from pathlib import Path

import click
from mashumaro.mixins.yaml import DataClassYAMLMixin


@dataclass
class Base(DataClassYAMLMixin):
    pass


@dataclass(kw_only=True)
class Template(Base):
    name: str
    entries: list[str]
    csl_type: str = ""
    csl_vals: list[str] = field(default_factory=list)
    blx_driver: str = ""
    blx_vals: list[str] = field(default_factory=list)
    bst_driver: str = ""
    bst_vals: list[str] = field(default_factory=list)


@dataclass(kw_only=True)
class Value(Base):
    val: str
    raw_csl: str = ""
    raw_blx: str = ""
    raw_bst: str = ""


@dataclass(kw_only=True)
class Group(Base):
    prefix: str | None = None
    delim: str | None = None
    suffix: str | None = None
    do: list[str, "Choice", "Group", Value] = field(default_factory=list)
    """String values should be Macro IDs."""


@dataclass(kw_only=True)
class Filter(Base):
    only: list[str] = field(default_factory=list)
    """String values should be Template names."""
    do: list[str, "Choice", Group, Value] = field(default_factory=list)
    """String values should be Macro IDs."""


@dataclass(kw_only=True)
class Choice(Base):
    filters: list[Filter]


@dataclass(kw_only=True)
class Macro(Base):
    id: str
    id_csl: str = ""
    id_blx: str = ""
    id_bst: str = ""
    do: list[str, Choice, Group, Value] = field(default_factory=list)
    """String values should be Macro IDs."""


@dataclass(kw_only=True)
class Model(Base):
    templates: list[Template] = field(default_factory=list)
    root: list[str, Choice, Group, Value] = field(default_factory=list)
    """String values should be Macro IDs."""
    macros: list[Macro] = field(default_factory=list)


@click.group()
@click.pass_context
def main(ctx: click.Context):
    """Uses metamodel to generate various views suited for
    CSL, biblatex and BibTeX."""
    this_file = Path(__file__)
    dir_src = this_file.parent
    fp_model = dir_src / "metamodel.yaml"
    with fp_model.open() as f:
        model = Model.from_yaml(f.read())
    ctx.obj = model

    click.echo(f"Loaded {len(model.templates)} templates.")


@main.command()
def test():
    pass


if __name__ == "__main__":
    main()

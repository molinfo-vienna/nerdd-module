from typing import Any
from xml.dom import minidom

from rdkit.Chem import Mol
from rdkit.Chem.Draw import MolDraw2DSVG

from .converter import Converter
from .converter_config import ConverterConfig

__all__ = ["MolToImageConverter"]

default_width = 300
default_height = 180


class MolToImageConverter(Converter):
    def _convert(self, input: Any, context: dict) -> Any:
        width = self.result_property.image_width
        height = self.result_property.image_height

        if width is None:
            width = default_width
        if height is None:
            height = default_height

        mol = input
        if mol is None:
            return None

        assert isinstance(mol, Mol), f"Expected RDKit Mol object, but got {type(mol)}"

        svg = MolDraw2DSVG(width, height)

        # remove background
        opts = svg.drawOptions()
        opts.clearBackground = False

        # add highlight circles around atoms during drawing
        # (we will remove them later in post processing)
        atoms = range(mol.GetNumAtoms())
        colors = [[(0.8, 1, 1)]] * mol.GetNumAtoms()
        radii = [0.5] * mol.GetNumAtoms()
        atom_highlight = dict(zip(atoms, colors))
        atom_radii = dict(zip(atoms, radii))
        svg.DrawMoleculeWithHighlights(mol, "", atom_highlight, {}, atom_radii, [])
        svg.FinishDrawing()

        # post process SVG
        xml = svg.GetDrawingText()
        tree = minidom.parseString(xml)
        root = tree.getElementsByTagName("svg")[0]

        # make highlight circles invisible
        for ellipse in root.getElementsByTagName("ellipse"):
            ellipse.setAttribute("style", "opacity:0")

        xml = tree.toxml()

        return xml

    # TODO: move to nerdd-link
    config = ConverterConfig(data_types="mol", output_formats="json")

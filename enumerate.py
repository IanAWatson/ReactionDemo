import itertools
import sys

from typing import List, NoReturn

from absl import app
from absl import flags
from absl import logging

from rdkit import Chem
from rdkit.Chem import rdChemReactions

NAME_PROP = '_Name'

FLAGS = flags.FLAGS

flags.DEFINE_string("acid", None, "Smiles file of acid reagents")
flags.DEFINE_string("amine", None, "Smiles file of amine reagents")

def do_enumeration(acids: List[Chem.rdchem.Mol],
                   amines: List[Chem.rdchem.Mol],
                   rxn: Chem.rdChemReactions.ChemicalReaction) -> NoReturn:
  """React `acids` with `amines` via `rxn` and print results.

  Args:
    acids: List of acids.
    amines:ist of amines.
    rxn: acid amine reaction.
  """
  for (acid, amine) in itertools.product(acids, amines):
    product = rxn.RunReactants((acid, amine))
    if len(product) != 1:
      print(f"Got {len(product)} from {Chem.MolToSmiles(acid)} {Chem.MolToSmiles(amine)}", file=sys.stderr)
      for p in product:
        print(Chem.MolToSmiles(product[i]), file=sys.stderr)
    else:
      name = acid.GetProp(NAME_PROP) + ' + ' + amine.GetProp(NAME_PROP)
      print(Chem.MolToSmiles(product[0][0], canonical=False), name)

def mols_from_file(fname: str) -> List[Chem.rdchem.Mol]:
  """Read smiles from `fname` and return a list of Molecules.
  Args:
    fname:
  Returns:
    List of rdkit.mol
  """
  with open(fname, "r") as input:
    result = []
    for line in input:
      f = line.rstrip().split(' ')
      mol = Chem.MolFromSmiles(f[0])
      mol.SetProp(NAME_PROP, f[1])
      result.append(mol)

  return result

def enumerate(unused_argv):
  del unused_argv

  acid_fname = FLAGS.acid
  amine_fname = FLAGS.amine

  acids = mols_from_file(acid_fname)
  amines = mols_from_file(amine_fname)
  print(f"Read {len(acids)} acids and {len(amines)} amine reagents", file=sys.stderr)

  smarts = '[OD1H:1]-[C:2]=[O:3].[ND1H2:4]-[CX4z1:5]>>[O:3]=[C:2]-[N:4]-[C:5].[O:1]'
  rxn = rdChemReactions.ReactionFromSmarts(smarts)

  do_enumeration(acids, amines, rxn)

if __name__ == "__main__":
  flags.mark_flag_as_required("acid")
  flags.mark_flag_as_required("amine")
  app.run(enumerate)

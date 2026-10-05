"""Calculate ESP and electron-density cube grids with Psi4 (not just point charges)."""
from common import *

def main():
    p=parser(__doc__); quantum_args(p)
    p.add_argument('--spacing', type=positive, default=0.2, help='Cube spacing in bohr')
    a=p.parse_args(); psi4,mol,out=psi4_setup(a)
    energy,wfn=psi4.energy(a.method,molecule=mol,return_wfn=True)
    psi4.set_options({'cubeprop_tasks':['ESP','DENSITY'], 'cubeprop_filepath':str(out.resolve()),
                      'cubic_grid_spacing':[a.spacing]*3, 'cubic_grid_overage':[4.0]*3})
    psi4.cubeprop(wfn)
    dump(out/'metadata.json',dict(energy_hartree=float(energy), method=a.method,
        potential_units='atomic units', grid_spacing_bohr=a.spacing,
        visualization='Open cubes in VMD/Avogadro; colour a density isosurface by ESP'))

if __name__ == '__main__': main()

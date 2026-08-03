# Symmetry Detector
##### Author: Piotr Wisniewski, 2026 (studying at UCL at this time)
##### Coding overseen by UCLAtto's Carla Figueira de Morisson Faria, Jiakang Chen, and Sufia Hashim during an internship there.
##### AI-Assisted coding (Claude). AI used primarily in an assistive role (spotting mistakes, discussing concepts, suggesting ideas)
##### The decisions about the code's final state were independently reasoned by the author.

### $\textbf{Requirements:}$
#### -Numpy
#### -Python 3.9+

### $\textbf{Installation:}$
#### In the terminal, inside your virtual environment:
#### `pip install git+https://github.com/wisniewski-piotr/EFsymmetry.git`
#### In the Python/Jupyter Notebook cell:
#### `from piotr import symmetry as sym`
####
### $\textbf{Uninstall:}$
#### In the terminal, inside your virtual environment:
#### `pip uninstall EFsymmetry`
#
## Description:
#### This python module is intended to be used to detect electric (or vector potential) field symmetries, and was created with
#### strong-field physics in mind. Electric field has different symmetries to vector potential, by the way.
#### The code can detect symmetries of any periodic field that is a combination of sine waves supplied to the programme.
#### Upon detecting a symmetry, it can also be used to expand a set of points (e.g., of field extrema) beyond what's currently given, using
#### the said field symmetries. IMPORTANT: This symmetry-based approach is helpful, but it can't always detect all the extrema (or such
#### points), and whether it can is conditional on the particular symmetry (and thus the shape of the field).
#####
### Current Limitations:
#### -The code can only accept commensurate fields
#### -The code can only reflect real-values about the said symmetries
#### -Given windowed parametrisation for a PINN, window widths are a placeholder and not able to be calculated by this code.
#
## $$\textbf{Code}$$
### BEFORE YOU START:
### Step 1:
#### Follow the Installation section above until you type `from piotr import symmetry as sym` into your code cell
### Step 2:
#### Use either `sym.set_cycle_period( cycle_period )` or `sym.set_omega( omega )` to initialise the module. This will create sym.cycle_period and sym.omega
### Step 3:
#### **Create the electric (or vector potential) field** via `sym.reset_wave()`, then `sym.add_wave( E1 , s1 , ϕ1 , E2 , s2 , ϕ2 )` to add Ex = E1 * Sin( s1 * sym.omega * t + ϕ1 ) , Ey = E2 * Sin( s2 * sym.omega * t + ϕ2 ) to the field E (Ex being the x-component and Ey being the y-component)
####
### Functions
#### `sym.set_extrema_locs( list )` - sets this list to be sym.extrema_locs, which is then automatically tested for being a list of all locations of field extrema for times from 0 to sym.cycle_period. It will flag errors down to the 8th decimal place.
#### `sym.set_zero_crossings_locs( list )` - sets this list to be sym.zero_crossings_locs, which is then automatically tested for being a list of all locations of field zero-crossings for times from 0 to cycle_period. It will flag errors down to the 8th decimal place.
#### `sym.syminput( list )` - converts a list into a format that can be understood by the other functions (into an **inputlist**).
#### The default list used for `sym.syminput()` is `sym.timespace`, a list of 50 random points between 0 and sym.cycle_period (recommended when testing for symmetries).
#### This function also takes a second argument, the operatorlist (more on that later).
#### `sym.translate( translation , inputlist )` - appends a Translation operator, by 'translation' time units, to inputlist.
#### `sym.rotate( radians , inputlist )` - appends a Field Rotation operator, by 'radians', to inputlist.
#### `sym.invert( inputlist )` - appends a Field Inversion operator to inputlist (encoding a pi radians rotation).
#### `sym.field_refl( radians, inputlist )` - appends a Field Reflection operator, about 'radians' to the x-axis, to inputlist.
#### `sym.time_refl( sym_reflectlist , inputlist )` - appends a Time Reflection symmetry operator, as defined in sym_reflectlist, to inputlist. More on sym_reflectlist later.
#### `sym.test( inputlist )` - tests whether the field has the same value, for each time in the original list supplied to sym.syminput, after that point in time is transformed through the operators appended to inputlist.
#### `sym.expand( initList , inputlist )` - verifies the symmetry supplied in inputlist, and then uses it to find more points with the same field values starting with the points in initList. For example, initList can contain an extremum, and the function will find more extrema if they're revealed by this symmetry.
#### `sym.ex_cr( inputlist )` - does the above automatically, using sym.extrema_locs and sym.zero_crossings_locs as inputs.
####
### For a PINN with windowed parametrisation:
#### `sym.set_window_centers_locs( list )` - sets the locations of window centers you could supply to (sym.window_centers_locs)
#### `sym.set_base_window_definitions( list )` - sets window centers, except in a format { "center" : T , "width" : L }
#### `sym.window_centers( inputlist )` - uses sym.expand to expand the list of window centers.
#### !!! ATTENTION: The above commands do NOT keep window center widths unchanged.
#### They are all set to cycle_period / (2 * N_window_centers)
####
### Additional Functions
#### `sym.set_sym_tolerance( tol )` - sets the tolerance used in all symmetry-related calculations (default: 1e-8)
#### `sym.expand_complex( initList , inputlist )` - the same thing as sym.expand, except this one takes in imaginary values but doesn't change them throughout the calculations. It is a first step towards making the code able to expand complex-time saddle lists.
##
### Example:
```python
import numpy as np
from piotr import symmetry as sym

sym.set_cycle_period( 100 )
cycle_period = sym.cycle_period

sym.reset_wave()                                  # Let's create an (w, 2w) bicircular field
sym.add_wave( 1 ,  1 , np.pi / 2 , 1 ,  1 , 0 )   # w,  counterclockwise
sym.add_wave( 1 , -2 , np.pi / 2 , 1 , -2 , 0 )   # 2w, clockwise

sym.test( sym.rotate( 2 * np.pi / 3 , sym.translate( cycle_period / 3 , sym.syminput() ) ) )
# returns True, as this is a trefoil.
```
##
## Validation
#### for (w,n*w) bicircular field, the (n+1)-fold rotation and translation symmetry has been observed for field where n = 2, 3, or 4.
#### for those same fields, Claude derived the fact that there are 2(n+1) time-reflection axes at τ = mT/(2(n+1)), each carrying a field
#### reflection with e^(2iα) = e^(2πim/(n+1)). All of those were verified by my code for n = 2, 3, and 4, for all values of m.
#### Each of those fields also rejects the other two's reflection axes (correctly).
#
## Technical Explanations:
#### This section is mainly for people curious about the specifics of how the code works, or for those who want to edit it.
#### sym.syminput( [ 4 ] ) will try to transform a list with just one number into the right format.
#### this format is [ 4 ] -> [ [ [1, 4, 0, 0] ], [] ]
#### now for a list of two points: [ 2 , 4 ] -> [ [ [1, 2, 0, 0], [1, 4, 1, 0] ], [] ]
#### So, the top level list used to have just the times (the 2 and the 4). After the formatting, it has two lists.
####
#### The second list is the operatorlist - this is where all the operators appended to this inputlist are stored.
#### The operatorlist is empty by default, and it can be passed to sym.syminput() as a second argument.
##
#### The first list is the nextlist. It contains more lists.
#### In the second slot (index: 1, as the first slot has index of 0) of each such list is the individual time.
#####
#### The first slot contains a 1 by default, and it signifies the field parity - it flips between 1 and -1 when the field is reflected.
#### This is because field reflection doesn't plainly combine with the previous rotations.
#####
#### The fourth slot is the field rotation, in radians. It is quite self-explanatory.
#####
#### The third slot is the index. It is kept to link each point in nextlist to its expansions in the modified list of points created
#### after applying all of the operators in operatorlist. sym.time_refl makes it so multiple points can result from, say, the first point.
#### All such points will, along with the first point, have an index of zero. sym.test then checks whether all points with a matching
#### index (on both lists) will have the same field x- and y-components. Only if they do, does sym.test return True.
#####
#### sym.expand works very simply - it takes initList, puts it in sym.syminput(), and applies operators to it, saving the results each
#### time. As the symmetry was verified by sym.test that runs at the start of sym.expand, we know the symmetry holds, and will result in
#### genuine expansion. The operators are continually applied (and results are saved) until the list no longer grows.
#####
#### sym.expand_complex adds the complex component to a fifth slot in each list nested inside of nextlist, and simply passes that fifth
#### slot through.
###
#### The real interesting stuff lies in sym.time_refl's sym_reflectlist.
#### At the very least, we have `sym.time_refl( [] , sym.syminput() )`, meaning that sym_reflectlist is empty,
#### so `sym_reflectlist = []`. Let's consider some other examples.
###
**1)**
```python
sym_reflectlist = [ sym.syminput( sym.extrema_locs ) ]
```
#### signifies a time reflection symmetry about the extrema.
###
**2)**
```python
sym_reflectlist = [ sym.invert( sym.syminput( sym.zero_crossings_locs ) ) ]
```
#### signifies a time reflection anti-symmetry about the zero-crossings.
###
**3)**
```python
sym_reflectlist = [ sym.syminput( sym.extrema_locs ) ,
sym.invert( sym.syminput( sym.zero_crossings_locs ) ) ,
sym.rotate( np.pi / 3 , sym.syminput( [ sym.cycle_period / 6 ] ) ) ]
```
#### signifies a time reflection symmetry about extrema, anti-symmetry about zero-crossings, and a time reflection followed by field
#### rotation by np.pi/3 symmetry about the point in time equal sym.cycle_period / 6.

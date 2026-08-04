# Symmetry Detector
##### <u>Author:</u> Piotr Wisniewski, 2026 (studying at UCL at this time)
##### Coding overseen by UCLAtto's Carla Figueira de Morisson Faria, Jiakang Chen, and Sufia Hashim during an internship there.
##### AI-Assisted coding (Claude). AI used primarily in an assistive role (spotting mistakes, discussing concepts, suggesting ideas).
##### The decisions about the code's final state were independently reasoned by the author.

### <u>Requirements:</u>
#### -$$\textbf{NumPy}$$
#### -$$\textbf{Python 3.9}+$$

### <u>Installation:</u>
#### In the terminal, inside your virtual environment:
#### `pip install git+https://github.com/wisniewski-piotr/EFsymmetry.git`
#### In the Python/Jupyter Notebook cell:
#### `from piotr import symmetry as sym`
####
### <u>Uninstall:</u>
#### In the terminal, inside your virtual environment:
#### `pip uninstall EFsymmetry`
#
## <u>Description:</u>
#### This Python module is intended to be used to detect electric (or vector potential) field symmetries, and was created with strong-field physics in mind.
#### *Electric field has different symmetries to vector potential, by the way.
#### The code can detect symmetries of any periodic field that is a combination of sine waves supplied to the programme.
#### Upon detecting a symmetry, it can also be used to expand a set of points (e.g., of field extrema) beyond what's currently given, using the said field symmetries. 
#### IMPORTANT: This symmetry-based approach is helpful, but it can't always detect all the extrema (or such points), and whether it can is conditional on the particular symmetry (and thus the shape of the field).
#####
### <u>Current Limitations:</u>
#### -The code can only accept commensurate (periodic) fields
#### -The code can only reflect real times (not complex saddle times) about the said symmetries
#### -Given windowed parametrisation for a PINN, window widths are a placeholder and not able to be calculated by this code.
#
## $$\textbf{Code}$$
### BEFORE YOU START:
### Step 1:
#### Follow the Installation section above until you type `from piotr import symmetry as sym` into your code cell
### Step 2:
#### Use either `sym.set_cycle_period( cycle_period )` or `sym.set_omega( omega )` to initialise the module. This will create sym.cycle_period and sym.omega
### Step 3:
#### **Create the electric (or vector potential) field** via `sym.reset_wave()`, then `sym.add_wave( E1 , s1 , ϕ1 , E2 , s2 , ϕ2 )` to add Ex = E1 * Sin( s1 * sym.omega * t + ϕ1 ) , Ey = E2 * Sin( s2 * sym.omega * t + ϕ2 ) to the field E (Ex being the x-component and Ey being the y-component).
#### sym.add_wave will only accept integer values of s1 and s2, so that the field is commensurate (meaning it is periodic with a cycle period of sym.cycle_period). E.g., for a 3:2 ratio of s1 and s2, set s1 = 3 and s2 = 2, and adjust the cycle period accordingly.
####
## <u>Functions</u>
#### `sym.set_extrema_locs( list )` - sets this list to be sym.extrema_locs, which is then automatically tested for containing ONLY locations of field extrema for times from 0 to sym.cycle_period. It will flag errors down to 1e-8.
#### `sym.set_zero_crossings_locs( list )` - sets this list to be sym.zero_crossings_locs, which is then automatically tested for containing ONLY locations of field zero-crossings for times from 0 to cycle_period. It will flag errors down to 1e-8.
#### `sym.syminput( list )` - converts a list into a format that can be understood by the other functions (into an **inputlist**).
#### The default list used for `sym.syminput()` is `sym.timespace`, a list of 50 random points between 0 and sym.cycle_period (recommended when testing for symmetries).
#### This function can also take a second argument, the operatorlist (more on that later).
#### `sym.translate( translation , inputlist )` - appends a Translation operator, by 'translation' time units, to inputlist.
#### `sym.rotate( radians , inputlist )` - appends a Field Rotation operator, by 'radians', to inputlist.
#### `sym.invert( inputlist )` - appends a Field Inversion operator to inputlist (encoding a pi radians rotation).
#### `sym.field_refl( radians, inputlist )` - appends a Field Reflection operator, about the axis you get by rotating the x-axis counterclockwise by 'radians', to inputlist.
#### `sym.time_refl( sym_reflectlist , inputlist )` - appends a Time Reflection symmetry operator, as defined in sym_reflectlist, to inputlist. More on sym_reflectlist in the Technical Explanations section at the bottom of this page (it's long).
#### `sym.test( inputlist )` - tests whether the field has the same value, for each time in the original list supplied to sym.syminput, after that point in time is transformed through the operators appended to inputlist.
#### `sym.expand( initList , inputlist )` - verifies the symmetry supplied in inputlist, and then uses it to find more points with the same field values starting with the points in initList. For example, initList can contain an extremum, and the function will find more extrema if they're revealed by this symmetry.
#### `sym.ex_cr( inputlist )` - does the above automatically, using sym.extrema_locs and sym.zero_crossings_locs as inputs.
####
### For a PINN with windowed parametrisation:
#### `sym.set_window_centers_locs( list )` - sets the locations of window centers (fills sym.window_centers_locs and sym.base_window_definitions).
#### `sym.set_base_window_definitions( list )` - sets window centers (fills sym.base_window_definitions and sym.window_centers_locs), except in a format:
```python
{ "center" : location , "width" : width }
```
#### `sym.window_centers( inputlist )` - uses sym.expand to expand the list of window centers.
#### !!! ATTENTION: The above commands do NOT keep window center widths unchanged.
#### They are all set to cycle_period / (2 * N_window_centers)
####
### Additional Functions
#### `sym.set_sym_tolerance( tol )` - sets the tolerance used in all symmetry-related calculations (default: 1e-8)
#### `sym.expand_complex( initList , inputlist )` - the same thing as sym.expand, except this one takes in imaginary values but doesn't change them throughout the calculations. It is a first step towards making the code able to expand complex-time saddle lists.
##
### <u>Example:</u>
```python
import numpy as np
from piotr import symmetry as sym

sym.set_cycle_period( 100 )
cycle_period = sym.cycle_period

sym.reset_wave()                                  # Let's create an (ω, 2ω) counter-rotating bicircular field
sym.add_wave( 1 ,  1 , np.pi / 2 , 1 ,  1 , 0 )   # ω,  counterclockwise
sym.add_wave( 1 , -2 , np.pi / 2 , 1 , -2 , 0 )   # 2ω, clockwise

sym.test( sym.rotate( 2 * np.pi / 3 , sym.translate( cycle_period / 3 , sym.syminput() ) ) )
# returns True, as this is a trefoil.
```
##
## <u>Validation</u>
#### For (ω,nω) counter-rotating bicircular field, the (n+1)-fold rotation followed by a cycle_period / (n+1) translation symmetry has been observed for fields where n = 2, 3, or 4.
#### For those same fields, Claude derived the fact that there are 2(n+1) time-reflection axes at τ = mT/(2(n+1)), each carrying a field reflection with e^(2iα) = e^(2πim/(n+1)).
#### All of those were verified by my code for n = 2, 3, and 4, for all values of m. Each of those fields also rejects the other two's reflection axes (correctly) - this is to mean that the field (ω,2ω) rejects the time-reflection axes of (ω,3ω) and (ω,4ω).
#####
#### To check the code is running correctly, you can download and run the check.py file inside this repository to verify that everything works fine (it will verify (ω,nω) fields for n = 2, 3, and 4, as well as do an integer harmonics check, as of the version dated August 4th 2026).
#
## <u>Technical Explanations:</u>
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
#### In the 2nd slot (slot_index: 1, as the first slot has slot_index of 0) of each such list is the individual time.
#####
#### The 1st slot contains a 1 by default, and it signifies the field parity - it flips between 1 and -1 when the field is reflected.
#### This is because field reflection doesn't plainly combine with the previous rotations.
#####
#### The 4th slot is the field rotation, in radians. It is quite self-explanatory.
#####
#### The 3rd slot is the index. It is kept to link each point in nextlist to its expansions in the modified list of points created after applying all of the operators in operatorlist.
#### sym.time_refl makes it so multiple points can be created from, say, the first point. All such points will, along with the first point, have an index of zero.
#### sym.test then checks whether all points with a matching index (on both lists) will have the same field x- and y-components. Only if they do, does sym.test return True.
#### This is a necessary safeguard (for instance: point 1's field shape may not match the field shape of its expansion, but may match the expansion of point 2; this could lead to a faulty symmetry being labelled as correct; by expansion I mean the transformation upon application of a valid symmetry, e.g., a reflection)
#####
#### sym.expand works very simply - it takes initList, puts it in sym.syminput(), and applies operators to it, saving the results each time. As the symmetry was verified by sym.test that runs at the start of sym.expand, we know the symmetry holds, and will result in genuine expansion.
#### The operators are continually applied (and results are saved) until the list no longer grows.
#####
#### sym.expand_complex adds the complex component to a fifth slot in each list nested inside of nextlist, and simply passes that fifth slot through.
###
#### The real interesting stuff lies in sym.time_refl's sym_reflectlist.
#### At the very least, we have `sym.time_refl( [] , sym.syminput() )`, meaning that sym_reflectlist is empty. So,
```python
sym_reflectlist = []
```
#### Let's consider some other examples.
###
**1)**
```python
sym_reflectlist = [ sym.syminput( sym.extrema_locs ) ]
```
#### signifies a time reflection symmetry about the extrema.
#### Keep in mind that both reflected and non-reflected points are kept by this symmetry - which is why the list of points can grow!
###
**2)**
```python
sym_reflectlist = [ sym.invert( sym.syminput( sym.zero_crossings_locs ) ) ]
```
#### signifies a time reflection anti-symmetry about the zero-crossings.
#### Differs from applying a field inversion outside sym.time_refl because doing that would invert both the reflected and non-reflected points, while this inverts ONLY the reflected ones.
###
**3)**
```python
sym_reflectlist = [ sym.syminput( sym.extrema_locs ) ,
sym.invert( sym.syminput( sym.zero_crossings_locs ) ) ,
sym.rotate( np.pi / 3 , sym.syminput( [ sym.cycle_period / 6 ] ) ) ]
```
#### signifies a time reflection symmetry about extrema, anti-symmetry about zero-crossings, and a time reflection about the point in time equal sym.cycle_period / 6 followed by field rotation of np.pi/3 symmetry.
#### IMPORTANT: sym.time_refl's sym_reflectlist can have any combination of any operators nested within it, granted none of those operators are themselves sym.time_refl. Nesting time reflection inside time reflection isn't supported (and is equivalent to translation).

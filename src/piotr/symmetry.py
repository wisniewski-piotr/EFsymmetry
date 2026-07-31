#!/usr/bin/env python

import random
import numpy as np

# ### Define Your Electric Field

sym_waves_definitions = [ ]

def reset_wave():
    """
    reset_wave()

    resets the shape of the electric field (to Ex=0 , Ey = 0)
    -------------------------------------------------------------------------------
    """
    sym_waves_definitions.clear()

def add_wave( E1 , s1 , ϕ1, E2, s2, ϕ2 ):
    """
    add_wave( E1 , s1 , ϕ1, E2, s2, ϕ2 )

    Adds a wave Ex=E1 * Sin( s1 * omega * t + ϕ1 ) , Ey=E2 * Sin( s2 * omega * t + ϕ2 ) to the electric field
    -------------------------------------------------------------------------------
    """
    sym_waves_definitions.append( [ E1 , s1 , ϕ1 , E2 , s2 , ϕ2 ] )

def _EFCalc(t):  # Electric field value calculation; used to confirm extrema and zero crossings locations as valid
    """
    _EFCalc(t)

    Calculates the electric field value at time t, and returns it as a numpy array
    -------------------------------------------------------------------------------
    """
    EleField = np.zeros( 2 )
    for i in sym_waves_definitions:
        EleField = EleField + np.array( [ i[ 0 ] * np.sin( i[ 1 ] * omega * t + i[ 2 ] ) 
                                           , i[ 3 ] * np.sin( i[ 4 ] * omega * t + i[ 5 ] ) ] )
    return EleField

def _CEFCalc(t):  # Complex-form Electric field value calculation; used in test(), uses _EFCalc()
    """
    _CEFCalc(t)

    Calculates the electric field value at time t, and returns it as a complex number
    -------------------------------------------------------------------------------
    """
    EleField = _EFCalc(t)
    ComplexFormEleField = EleField[ 0 ] + 1j * EleField[ 1 ]
    return ComplexFormEleField

def _EFGrad(t):  # Gradient of the electric field
    """
    _EFGrad(t)

    Calculates the electric field gradient's value at time t, and returns it as a numpy array
    -------------------------------------------------------------------------------
    """
    EleFieldGrad = np.zeros( 2 )
    for i in sym_waves_definitions:
        EleFieldGrad = EleFieldGrad + np.array( [ i[ 0 ] * i[ 1 ] * omega * np.cos( i[ 1 ] * omega * t + i[ 2 ] ) ,
                                        i[ 3 ] * i[ 4 ] * omega * np.cos( i[ 4 ] * omega * t + i[ 5 ] ) ] )
    return EleFieldGrad


# #### Type in your values
# ##### add_wave(A, B, C, D, E, F) --> adds "[ A sin(B w t + C) , D sin(E w t + F) ]" to the Electric field; C is in radians
# ##### The comma in the middle separates the x-component of the field (A, B, C) from the y-component (D, E, F)
# #####
# ##### w is "omega" defined in the first notebook cell

zero_crossings_locs  = []
extrema_locs         = []
window_centers_locs = []
base_window_definitions = []
timespace            = None

def set_sym_tolerance( tol ):
    global sym_tolerance
    sym_tolerance = tol

def set_cycle_period( cp ):
    global cycle_period
    global omega
    if cp is None:
        cycle_period = None
        omega = None
    else:
        cycle_period = cp
        omega = 2 * np.pi / cp
        global timespace
        timespace = []
        _rng = random.Random(42)
        for i in range(50):
            timespace.append(_rng.random() * cycle_period)
        timespace.sort()

def set_omega( w ):
    set_cycle_period( None if w is None else 2 * np.pi / w )

set_omega( None )
set_sym_tolerance( 1e-8 )

def _set_ExCr( list1 , list2 ):
    if omega is None or cycle_period is None or timespace is None:
        print("!!! You must first set a cycle period (set_cycle_period(T)) or angular frequency (set_omega(w))")
        assert False
    if type(list1) == list or type(list1) == np.ndarray:
        source = list( list1 )
    else:
        print("The syminput of set_extrema() must be a list of different points in time between 0 and the cycle period")
        assert False
    list2.clear()
    for i in source:
        if all( min( ( j - i ) % cycle_period , ( cycle_period - ( j - i ) ) % cycle_period ) > sym_tolerance for j in list2):
            list2.append( i )

def set_extrema_locs( list1 ):
    global extrema_locs
    _set_ExCr( list1 , extrema_locs )
    success = 0
    for i in extrema_locs:
        if abs( np.dot( _EFCalc( i ), _EFGrad( i ) ) / omega ) < sym_tolerance and abs( _CEFCalc( i ) ) > sym_tolerance: 
            # d(|E|^2)/dt = 2 * E * E'. So, if E*E'=0, d|E|/dt=0. Thanks Claude for this idea
            success += 1
    if success != len( extrema_locs ):
        print("!!!  Incorrect Extrema Locations")
        assert False

def set_zero_crossings_locs( list1 ):
    global zero_crossings_locs
    _set_ExCr( list1 , zero_crossings_locs )
    success = 0
    for i in zero_crossings_locs:
        if abs( np.linalg.norm( _EFCalc( i ) ) ) < sym_tolerance:
            success += 1
    if success != len( zero_crossings_locs ):
        print("!!!  Incorrect Zero-crossings' Locations")
        assert False
    success = 0

def set_window_centers_locs( list1 ):
    if omega is None or cycle_period is None or timespace is None:
        print("!!! You must first set a cycle period (set_cycle_period(T)) or angular frequency (set_omega(w))")
        assert False
    global window_centers_locs
    _set_ExCr( list1 , window_centers_locs )
    global base_window_definitions
    base_window_definitions = []
    for i in window_centers_locs:
        base_window_definitions.append( { "center": i , "width": cycle_period / (2 * len( window_centers_locs ) ) } )

def set_base_window_definitions( list1 ):
    if omega is None or cycle_period is None or timespace is None:
        print("!!! You must first set a cycle period (set_cycle_period(T)) or angular frequency (set_omega(w))")
        assert False
    global window_centers_locs
    raw_window_centers_locs = []
    for i in list1:
        raw_window_centers_locs.append( i[ "center" ] )
    _set_ExCr( raw_window_centers_locs , window_centers_locs )
    global base_window_definitions
    base_window_definitions = []
    for i in window_centers_locs:
        base_window_definitions.append( { "center": i , "width": cycle_period / (2 * len( window_centers_locs ) ) } )

# ### Symmetry Operators

def syminput( tlist_original = None , operatorlist = None ):
    """
    syminput( tlist_original = timespace , operatorlist = None )

    converts a list of times, tlist_original, into a format that is readable to the function test()

    operatorlist is a list of operators to be applied to tlist_original during test.


    the default value of tlist_original is timespace, a list of 50 randomly generated points in time between 0 and cycle_period.

    -------------
    operatorlist must be at least an empty list [].
    operators inside operatorlist look like [ "Translate" , translation ].
    Example of operatorlist in syminput:  test( syminput( timespace , [ [ "Translate" , cycle_period / 2 ] , [ "Invert" ] ] ) )
    This example checks for half-cycle symmetry if used in test()

    All operators:  translate() , time_refl() , field_refl() , rotate() , invert()

    -------------
    for any time t inside tlist_original, it gets transformed into [ 1 , t , i , 0 ] inside nextlist, where:

    - 1 is the field parity (+-1), symbolising whether the field has been reflected
    - t is the time
    - i is the index, which is necessary to track which future points came from which original point in
      tlist_original ( as new points may be be created after time_refl ). It is a different integer for every point that was
      in tlist_original, and is shared by all points that come from that point via the operators
    - 0 is the angle, [ 0 , 2 * np.pi ), by which the field has been rotated.

    All of those variables will change after _ApplySymmetryOperators() applies symmetry operators to them

    -------------
    this function returns inputlist, where inputlist = [ nextlist , operatorlist ]
    -------------------------------------------------------------------------------
    """
    if tlist_original is None:
        if omega is None or cycle_period is None or timespace is None:
            print("!!! You must first set a cycle period (set_cycle_period(T)) or angular frequency (set_omega(w))")
            assert False
        tlist_original = timespace
    tlist_original = list( tlist_original )
    nextlist = []
    for i in range(len( tlist_original ) ):
        nextlist.append( [ 1 , tlist_original[ i ] , i , 0 ] )
    if operatorlist is None:
        inputlist = [ nextlist , [] ]
    else:
        inputlist = [ nextlist , operatorlist ]
    return inputlist

def translate( translation , inputlist ):
    """
    translate( translation , inputlist )

    Encodes time translation symmetry by 'translation'

    -------------
    Adds [ "Translate" , translation ] to the operatorlist ( check out the documentation of syminput() )
    -------------------------------------------------------------------------------
    """
    inputlist[ 1 ].append( [ "Translate" , translation ] )
    return inputlist

def invert( inputlist ):
    """
    invert( inputlist )

    Encodes field inversion symmetry
    Literally adds pi radians (180 degrees) to rotation

    -------------
    Adds [ "Invert" ] to the operatorlist ( check out the documentation of syminput() )
    -------------------------------------------------------------------------------
    """
    inputlist[ 1 ].append( [ "Invert" ] )
    return inputlist

def rotate( radians , inputlist ):
    """
    rotate( radians , inputlist )

    Encodes counterclockwise field rotation symmetry by 'radians'

    -------------
    Adds [ "Rotate" , radians ] to the operatorlist ( check out the documentation of syminput() )
    -------------------------------------------------------------------------------
    """
    inputlist[ 1 ].append( [ "Rotate" , radians ] )
    return inputlist

def field_refl( radians , inputlist ):
    """
    field_refl( radians , inputlist )

    Encodes field reflection symmetry about the axis that you get by rotating the x-axis counterclockwise by 'radians'

    -------------
    Adds [ "Field Reflect" , radians ] to the operatorlist ( check out the documentation of syminput() )
    -------------------------------------------------------------------------------
    """
    inputlist[ 1 ].append( [ "Field Reflect" , radians ] )
    return inputlist

def time_refl( sym_reflectlist , inputlist ):
    """
    time_refl( sym_reflectlist , inputlist )

    Encodes time reflection symmetry, as defined by sym_reflectlist

    Time Reflection symmetry is the hardest to implement, as it involves creating multiple points out of one,
    acting with operators only on the reflected points but keeping both reflected and non-reflected points, as
    well as counting how many times points have been reflected when trying to reach closure.

    -------------
    sym_reflectlist must at least be an empty list []

    it can contain lists of points by which there are reflection symmetries, inside syminput.
    Example:  test( time_refl( [ syminput( extrema_locs ) ] , syminput( timespace ) ) ) encodes time reflection
    symmetry about points in time on the list extrema_locs.
    here, sym_reflectlist = [ syminput( extrema_locs ) ]

    sym_reflectlist can also have syminput be modified by operators.
    Example:  test( time_refl( [ invert( syminput( zero_crossings_locs ) ) ] , syminput( timespace ) ) ) encodes
    time reflection anti-symmetry about points in time on the list zero_crossings_locs.
    here, sym_reflectlist = [ invert( syminput( zero_crossings_locs ) ) ]

    sym_reflectlist can have many different lists of point about which it reflects, subsequently applying different 
    operators to each of the lists.
    Example:  sym_reflectlist = [ syminput( extrema_locs ) , invert( syminput( zero_crossings_locs ) ) ,
                                translate( cycle_period / 3 , syminput( [ cycle_period / 3 ] ) ) ]

    sym_reflectlist can contain every single reflection operator except time_refl().
    Yes, time reflection nested inside a time reflection is not supported (and is equivalent to translation anyways).

    -------------
    Adds [ "Time Reflect" , sym_reflect ] to the operatorlist ( check out the documentation of syminput() )
    -------------------------------------------------------------------------------
    """
    inputlist[ 1 ].append( [ "Time Reflect" , sym_reflectlist ] )
    return inputlist

def _ApplySymmetryOperators( nextlist , tlist_operators , blockReflection = True ):
    """
    _ApplySymmetryOperators( nextlist , tlist_operators , blockReflection = True )

    Applies the symmetry operators in tlist_operators to nextlist, where
    nextlist is in the format created by syminput().


    blockReflection is a True/False boolean, and it tells us whether we are inside a time_refl(),
    meaning we should not accept more reflections (default state of blockReflection = True), or
    whether we are not and we should apply the reflection operator instead of delibrately terminating.

    For more info, look at the documentation of syminput()

    You may also find useful the documentations of test(), translate(), rotate(), invert(),
    field_refl(), and time_refl()
    -------------------------------------------------------------------------------
    """
    for operator in tlist_operators:

        if operator[ 0 ] == "Translate":
            sym_tlist = []
            for i in nextlist:
                sym_tlist.append( [ i[ 0 ] , ( i[ 1 ] + operator[ 1 ] ) % cycle_period , i[ 2 ] , i[ 3 ] ] )
            nextlist = []
            for i in sym_tlist:
                nextlist.append( [ i[ 0 ] , i[ 1 ] , i[ 2 ] , i[ 3 ] ] )

        elif operator[ 0 ] == "Time Reflect":
            # This operator's code is so long because time reflection symmetry creates more points (so we need to
            # check if they're already appended or not) and because there are operators inside time_refl(), applied
            # only to the reflected points, not the original ones.
            # Also, this code automatically reflects until closure (until the list of times stops growing)
            # I think, in hindsight, that was unnecessry and might have possibly made the code more complicated.
            if blockReflection:
                print("!!!  Please Do Not Nest Time Reflection Inside Another Time Reflection\nThis code won't work if you do")
                assert False
            sym_tlist = []
            for i in nextlist:
                sym_tlist.append( [ i[ 0 ] , i[ 1 ] , i[ 2 ] , i[ 3 ] ] )
            reflect_counter = 0
            for i in sym_tlist:
                for syminput_refl in operator[ 1 ]:
                    reflectlist = []
                    for X in _ApplySymmetryOperators( syminput_refl[ 0 ] , syminput_refl[ 1 ] , True ):
                        reflectlist.append( X[ 1 ] ) # the list of points about which we reflect

                    change_symOperators = _ApplySymmetryOperators( [ [1, 0.0, 0, 0.0] ], syminput_refl[1] , True )[ 0 ]
                    p_A, phi_A = change_symOperators[ 0 ], change_symOperators[ 3 ] # find out what effect the operators have on
                                                                                    # field parity and rotation
                    for j in reflectlist:

                        for t in _ApplySymmetryOperators( [ [ i[ 0 ] , ( -i[ 1 ] + 2 * j ) % cycle_period , i[ 2 ] , i[ 3 ] ] ] ,
                                                     syminput_refl[ 1 ] , True ): # apply in case of multiple points from reflection
                            t[ 0 ] = i[ 0 ] * p_A
                            t[ 3 ] = ( i[ 3 ] + phi_A * i[ 0 ] ) % ( 2 * np.pi )
                            # the point of this is to separate per-axis operations from whole-set operations.
                            # basically, the initial sign i[ 0 ] changes how the rotation in the operatorlist combines
                            # with the prior rotation in i[ 3 ]. This is why we need change_symOperators first.
                            #
                            # t is now the modified, reflected, acted upon set of points in time
                            append_counter = 0
                            for n in sym_tlist:
                                if min( ( t[ 1 ] - n[ 1 ] ) % cycle_period , # check if the time is already in the list
                                        cycle_period - ( t[ 1 ] - n[ 1 ] ) % cycle_period ) < sym_tolerance:
                                    if ( min( ( t[ 3 ] - n[ 3 ] ) % ( 2 * np.pi ) , ( -t[ 3 ] + n[ 3 ] + 2 * np.pi ) % ( 2 * np.pi )
                                          ) > sym_tolerance or t[ 0 ] != n[ 0 ]) and abs( _CEFCalc( n[ 1 ] ) ) >= sym_tolerance:
                                        # if yes, check if field differs or is the same
                                        anomalousfield_i = np.exp( 1j * t[ 3 ] ) * ( np.conj( _CEFCalc( t[ 1 ] )
                                                                                            ) if t[ 0 ] == -1 else _CEFCalc( t[ 1 ] ) )
                                        anomalousfield_n = np.exp( 1j * n[ 3 ] ) * ( np.conj( _CEFCalc( n[ 1 ] ) 
                                                                                            ) if n[ 0 ] == -1 else _CEFCalc( n[ 1 ] ) )
                                        if abs( anomalousfield_i - anomalousfield_n ) > sym_tolerance: # if differs, crash programme
                                            print("!!!   Symmetry Error: A single point in time has multiple field values\n"+
                                                  "(e.g., is both inverted and non-inverted)")
                                            assert False
                                else:
                                    append_counter += 1
                            if append_counter == len( sym_tlist ):
                                sym_tlist.append( [ t[ 0 ] , t[ 1 ] , t[ 2 ] , t[ 3 ] ] )
                                reflect_counter += 1
                                if reflect_counter >= 1000: # not 1000 or more reflections, in case the field is incommensurate
                                    print("!!!  REFLECTION LIMIT REACHED")
                                    return False # crash the programme
            nextlist = []
            for i in sym_tlist:
                nextlist.append( [ i[ 0 ] , i[ 1 ] , i[ 2 ] , i[ 3 ] ] )

        elif operator[ 0 ] == "Invert":
            sym_tlist = []
            for i in nextlist:
                sym_tlist.append( [ i[ 0 ] , i[ 1 ] , i[ 2 ] , ( i[ 3 ] - np.pi ) % ( 2 * np.pi ) ] )
            nextlist = []
            for i in sym_tlist:
                nextlist.append( [ i[ 0 ] , i[ 1 ] , i[ 2 ] , i[ 3 ] ] )

        elif operator[ 0 ] == "Rotate":
            sym_tlist = []
            for i in nextlist:
                sym_tlist.append( [ i[ 0 ] , i[ 1 ] , i[ 2 ] , ( i[ 3 ] - operator[ 1 ] ) % ( 2 * np.pi ) ] ) 
                # Allow E(t+T/3) = E(t) e^(i*2pi/3) for a bicircular (w,2w) field. If our code tests whether E(t) is equal something,
                # it must give us E(t) = E(t+T/3) e^(-i*2pi/3). This is why we **SUBTRACT** the angle our rotation symmetry is by.
                # because it's e^(-i*2pi/3), and not e^(i*2pi/3).
            nextlist = []
            for i in sym_tlist:
                nextlist.append( [ i[ 0 ] , i[ 1 ] , i[ 2 ] , i[ 3 ] ] )

        elif operator[ 0 ] == "Field Reflect":
            sym_tlist = []
            for i in nextlist:
                sym_tlist.append( [ -i[ 0 ] , i[ 1 ] , i[ 2 ] , ( -i[ 3 ] + 2 * operator[ 1 ] ) % ( 2 * np.pi ) ] ) 
                # -i[ 3 ] + 2 * operator[ 1 ] because conjugate( e^{ i theta } * z ) = e^{ -i theta } * conjugate( z ).
                # e^{ i theta }, acting on a complex number, represents rotation ( in a complex plane )
            nextlist = []
            for i in sym_tlist:
                nextlist.append( [ i[ 0 ] , i[ 1 ] , i[ 2 ] , i[ 3 ] ] )

        else:
            print("Unknown operator:  " + operator[ 0 ] )
            assert False
    return nextlist

# ### Testing for symmetries

def IsCommensurate():
    if not test( translate( cycle_period , syminput( timespace ) ) ):
        return False
    else:
        return True

def _TestSym( inputlist ):
    """
    test( inputlist )

    tests whether the symmetry defined in inputlist is correct, returning a True/False boolean.

    For more info, look at the documentation of syminput()

    You may also find useful the documentations of translate(), rotate(), invert(), field_refl(),
    time_refl(), and _ApplySymmetryOperators()

    -------------
    inputlist = [ nextlist , operatorlist ]
    nextlist is in the format of syminput(), and it is modified by _ApplySymmetryOperators(),
    according to instructions in operatorlist, to create tlist_modified.

    test() then compares, via _CEFCalc(), whether the electric field is the same, for each point in nextlist, as
    it is in tlist_modified for all the other points with that same index ( check out syminput() documentation ), aka.
    for all the points that came from operating on that original point in nextlist via operators in operatorlist.
    There can be many such points because of time_refl.

    -------------
    Example:  test( syminput( timespace ) ) always returns True, as no operators are applied.
              test( translate( cycle_period , syminput( timespace ) ) ) tests for field commensurability.
              test( invert( translate( cycle_period / 2 , syminput( timespace ) ) ) ) tests for half-cycle symmetry.

    -------------------------------------------------------------------------------
    """
    nextlist = inputlist[ 0 ]
    operatorlist   = inputlist[ 1 ]


    tlist_modified = []
    for i in nextlist:
        tlist_modified.append( [ i[ 0 ] , i[ 1 ] , i[ 2 ] , i[ 3 ] ] )

    tlist_modified = _ApplySymmetryOperators( tlist_modified , operatorlist , False )
    if tlist_modified == False:  # this happens if the number of reflections exceeds the limit (default: 1000).
        return False


    success = 0
    for i in nextlist:
        workinglist_sym_tlist = []
        for j in tlist_modified:
            if j[ 2 ] == i[ 2 ]:
                workinglist_sym_tlist.append( j ) # working_sym_tlist is the list of points with the same index as i from nextlist.
        success_working = 0
        for j in workinglist_sym_tlist: # calculate whether field values match for all of them; calculations based on field parity.
            if j[ 0 ] == 1:
                if abs( np.exp( 1j * j[ 3 ] ) * _CEFCalc( j[ 1 ] ) - _CEFCalc( i[ 1 ] ) ) < sym_tolerance:
                    success_working += 1
            elif j[ 0 ] == -1:
                if abs( np.exp( 1j * j[ 3 ] ) * np.conj( _CEFCalc( j[ 1 ] ) ) - _CEFCalc( i[ 1 ] ) ) < sym_tolerance:
                    success_working += 1
            else:
                print("!!! Field Parity Error: the field parity sign isn't +-1")
                assert False
        if success_working == len( workinglist_sym_tlist ): # if they match for all of them, mark i as successful in tlist
            success += 1
    if success == len( nextlist ): # if all i are successful, return True, as the symmetry matches
        return True
    else:
        return False

def test( inputlist ):
    if not _TestSym( translate( cycle_period , syminput( timespace ) ) ):
        print("!!! The field is INCOMMENSURATE\nThis breaks the programme\nProceed at your own risk\n\n" + 
              "Incommensurate means that translation by cycle_period does NOT yield the same field.")
        assert False
    return _TestSym( inputlist )

def expand( initList , inputlist ):
    """
    expand( initList , inputlist )

    tests whether test( inputlist ) returns True, and thus whether the symmetry defined in it is true.
    If not, it returns False.
    If yes, it copies the time points in initList ( NOT in the format of syminput, just a list of points
    in time ) using the operatorlist in inputlist ( check syminput() documentation ).

    For example, if initList is the list of maxima, it will keep applying the operatorlist so long as the
    initList is growing. When it reaches closure, it returns the new, expanded initList, now having the maxima
    that were previously there and all those reachable via the operators.

    this is NOT guaranteed to give you all the maxima/minima/zero-crossings/window centers of the field.

    -------------
    Example:  expand( extrema_locs , invert( translate( cycle_period / 2 , syminput( timespace ) ) ) ) tests for
    half-cycle symmetry across timespace, and if it finds it, it takes all the time points in extrema_locs
    ( presumably all the extrema locations from 0 to cycle_period ) and uses the half-cycle symmetry to find
    more extrema if possible ( by translating by cycle_period / 2 ).
    -------------------------------------------------------------------------------
    """
    if test( inputlist ) == False:
        print("!!!  Incorrect Symmetry! test returns False")
        return False
    operatorlist = inputlist[ 1 ]

    working_initList = []
    for i in initList:
        working_initList.append( i )

    tlist_modified = []
    for i in initList:
        tlist_modified.append( [ 1 , i , 0 , 0 ] )

    shouldthiscodecontinue = True
    continue_counter = 0
    while shouldthiscodecontinue:  # This while loop ensures we keep applying the operators until closure
        previousLength = len( working_initList )

        tlist_modified = _ApplySymmetryOperators( tlist_modified , operatorlist , False )
        if tlist_modified == False:  # this happens if the number of reflections exceeds the limit (default: 1000).
            assert False

        for i in tlist_modified:
            if all( min( ( j - i[ 1 ] ) % cycle_period , ( cycle_period - ( j - i[ 1 ] ) ) % cycle_period ) >
                    sym_tolerance for j in working_initList):
                working_initList.append( i[ 1 ] )

        if len( working_initList ) == previousLength:
            shouldthiscodecontinue = False
        continue_counter +=1
        if continue_counter >= 100:
            print("!!! This code should not continue for 100 times over!\nField incommensurate?")
            assert False

    working_initList.sort()
    return working_initList

def ex_cr( inputlist ):
    """
    ex_cr( inputlist )

    uses expand() to find more extrema and crossings via a supplied operatorlist inside inputlist,
    if that symmetry is true for inputlist ( otherwise it returns False ).

    the initial lists of extrema and crossings are extrema_locs and zero_crossings_locs, respectively.
    -------------------------------------------------------------------------------
    """
    working_extrema_locs = expand( extrema_locs , inputlist )
    if working_extrema_locs == False:
        return False
    print( "Extrema Locations:\n" + str( working_extrema_locs ) )


    working_zero_crossings_locs = expand( zero_crossings_locs , inputlist )
    if working_zero_crossings_locs == False:
        return False
    print( "Zero-Crossings Locations:\n" + str( working_zero_crossings_locs ) )

    return working_extrema_locs , working_zero_crossings_locs

def window_centers( inputlist ):
    """
    window_centers( inputlist )

    uses expand() to find more window center locations via a supplied operatorlist inside inputlist
    ( see syminput() documentation ), if that symmetry is true for inputlist ( otherwise it returns False ).

    the initial list of window centers is base_window_definitions.

    !!! This programme is not capable of evaluating window widths accurately
    -------------------------------------------------------------------------------
    """

    init_window_centers_locs = []
    for i in base_window_definitions:
        init_window_centers_locs.append( i[ "center" ] )

    window_centers_locs = expand( init_window_centers_locs , inputlist )
    if window_centers_locs == False:
        return False
    print( "!!! WARNING: This version is incapable of determining window widths accurately\n" + 
           "width = cycle_period / ( 2 * N_window_centers )\n\n" +
           "Window Centers:\n" + str( window_centers_locs ) )

    new_base_window_definitions = []
    for i in window_centers_locs:
        new_base_window_definitions.append( {"center": i , "width": cycle_period / ( 2 * len( window_centers_locs ) ) } )

    return new_base_window_definitions

def _ApplySymmetryOperatorsComp( nextlist_raw , tlist_operators , blockReflection = True ):
    """
    _ApplySymmetryOperatorsComp( nextlist , tlist_operators , blockReflection = True )

    Applies the symmetry operators in tlist_operators to nextlist, where
    nextlist is in the format created by syminput().


    blockReflection is a True/False boolean, and it tells us whether we are inside a time_refl(),
    meaning we should not accept more reflections (default state of blockReflection = True), or
    whether we are not and we should apply the reflection operator instead of delibrately terminating.

    For more info, look at the documentation of syminput()

    You may also find useful the documentations of test(), translate(), rotate(), invert(),
    field_refl(), and time_refl()
    -------------------------------------------------------------------------------
    """
    nextlist = []
    for i in nextlist_raw:
        if len( i ) == 5:
            nextlist.append( i )
        elif len( i ) == 4:
            nextlist.append( [ i[ 0 ] , i[ 1 ] , i[ 2 ] , i[ 3 ] , 0 ] )

    for operator in tlist_operators:

        if operator[ 0 ] == "Translate":
            sym_tlist = []
            for i in nextlist:
                sym_tlist.append( [ i[ 0 ] , ( i[ 1 ] + operator[ 1 ] ) % cycle_period , i[ 2 ] , i[ 3 ] , i[ 4 ] ] )
            nextlist = []
            for i in sym_tlist:
                nextlist.append( [ i[ 0 ] , i[ 1 ] , i[ 2 ] , i[ 3 ] , i[ 4 ] ] )

        elif operator[ 0 ] == "Time Reflect":
            if blockReflection:
                print("!!!  Please Do Not Nest Time Reflection Inside Another Time Reflection\nThis code won't work if you do")
                assert False
            sym_tlist = []
            for i in nextlist:
                sym_tlist.append( [ i[ 0 ] , i[ 1 ] , i[ 2 ] , i[ 3 ] , i[ 4 ] ] )
            reflect_counter = 0
            for i in sym_tlist:
                for syminput_refl in operator[ 1 ]:
                    reflectlist = []
                    for X in _ApplySymmetryOperatorsComp( syminput_refl[ 0 ] , syminput_refl[ 1 ] , True ):
                        reflectlist.append( X[ 1 ] ) # the list of points about which we reflect

                    change_symOperators = _ApplySymmetryOperatorsComp( [ [1, 0.0, 0, 0.0, 0.0] ], syminput_refl[1] , True )[ 0 ]
                    p_A, phi_A = change_symOperators[ 0 ], change_symOperators[ 3 ] # find out what effect the operators have on
                                                                                    # field parity and rotation
                    for j in reflectlist:

                        for t in _ApplySymmetryOperatorsComp( [ [ i[ 0 ] , ( -i[ 1 ] + 2 * j ) % cycle_period , i[ 2 ] , i[ 3 ] , i[ 4 ] ] ] ,
                                                     syminput_refl[ 1 ] , True ): # apply in case of multiple points from reflection
                            t[ 0 ] = i[ 0 ] * p_A
                            t[ 3 ] = ( i[ 3 ] + phi_A * i[ 0 ] ) % ( 2 * np.pi )
                            # the point of this is to separate per-axis operations from whole-set operations.
                            # basically, the initial sign i[ 0 ] changes how the rotation in the operatorlist combines
                            # with the prior rotation in i[ 3 ]. This is why we need change_symOperators first.
                            #
                            # t is now the modified, reflected, acted upon set of points in time
                            append_counter = 0
                            for n in sym_tlist:
                                if min( ( t[ 1 ] - n[ 1 ] ) % cycle_period , # check if the time is already in the list
                                        cycle_period - ( t[ 1 ] - n[ 1 ] ) % cycle_period ) < sym_tolerance:
                                    if ( min( ( t[ 3 ] - n[ 3 ] ) % ( 2 * np.pi ) , ( -t[ 3 ] + n[ 3 ] + 2 * np.pi ) % ( 2 * np.pi )
                                          ) > sym_tolerance or t[ 0 ] != n[ 0 ]) and abs( _CEFCalc( n[ 1 ] ) ) >= sym_tolerance:
                                        # if yes, check if field differs or is the same
                                        anomalousfield_i = np.exp( 1j * t[ 3 ] ) * ( np.conj( _CEFCalc( t[ 1 ] )
                                                                                            ) if t[ 0 ] == -1 else _CEFCalc( t[ 1 ] ) )
                                        anomalousfield_n = np.exp( 1j * n[ 3 ] ) * ( np.conj( _CEFCalc( n[ 1 ] ) 
                                                                                            ) if n[ 0 ] == -1 else _CEFCalc( n[ 1 ] ) )
                                        if abs( anomalousfield_i - anomalousfield_n ) > sym_tolerance: # if differs, crash programme
                                            print("!!!   Symmetry Error: A single point in time has multiple field values\n"+
                                                  "(e.g., is both inverted and non-inverted)")
                                            assert False
                                else:
                                    append_counter += 1
                            if append_counter == len( sym_tlist ):
                                sym_tlist.append( [ t[ 0 ] , t[ 1 ] , t[ 2 ] , t[ 3 ] , t[ 4 ] ] )
                                reflect_counter += 1
                                if reflect_counter >= 1000: # not 1000 or more reflections, in case the field is incommensurate
                                    print("!!!  REFLECTION LIMIT REACHED")
                                    return False # crash the programme
            nextlist = []
            for i in sym_tlist:
                nextlist.append( [ i[ 0 ] , i[ 1 ] , i[ 2 ] , i[ 3 ] , i[ 4 ] ] )

        elif operator[ 0 ] == "Invert":
            sym_tlist = []
            for i in nextlist:
                sym_tlist.append( [ i[ 0 ] , i[ 1 ] , i[ 2 ] , ( i[ 3 ] - np.pi ) % ( 2 * np.pi ) , i[ 4 ] ] )
            nextlist = []
            for i in sym_tlist:
                nextlist.append( [ i[ 0 ] , i[ 1 ] , i[ 2 ] , i[ 3 ] , i[ 4 ] ] )

        elif operator[ 0 ] == "Rotate":
            sym_tlist = []
            for i in nextlist:
                sym_tlist.append( [ i[ 0 ] , i[ 1 ] , i[ 2 ] , ( i[ 3 ] - operator[ 1 ] ) % ( 2 * np.pi ) , i[ 4 ] ] ) 
                # Allow E(t+T/3) = E(t) e^(i*2pi/3) for a bicircular (w,2w) field. If our code tests whether E(t) is equal something,
                # it must give us E(t) = E(t+T/3) e^(-i*2pi/3). This is why we **SUBTRACT** the angle our rotation symmetry is by.
                # because it's e^(-i*2pi/3), and not e^(i*2pi/3).
            nextlist = []
            for i in sym_tlist:
                nextlist.append( [ i[ 0 ] , i[ 1 ] , i[ 2 ] , i[ 3 ] , i[ 4 ] ] )

        elif operator[ 0 ] == "Field Reflect":
            sym_tlist = []
            for i in nextlist:
                sym_tlist.append( [ -i[ 0 ] , i[ 1 ] , i[ 2 ] , ( -i[ 3 ] + 2 * operator[ 1 ] ) % ( 2 * np.pi ) , i[ 4 ] ] ) 
                # -i[ 3 ] + 2 * operator[ 1 ] because conjugate( e^{ i theta } * z ) = e^{ -i theta } * conjugate( z ).
                # e^{ i theta }, acting on a complex number, represents rotation ( in a complex plane )
            nextlist = []
            for i in sym_tlist:
                nextlist.append( [ i[ 0 ] , i[ 1 ] , i[ 2 ] , i[ 3 ] , i[ 4 ] ] )

        else:
            print("Unknown operator:  " + operator[ 0 ] )
            assert False
    return nextlist

def expand_complex( initListComp , inputlist ):
    """
    expand_complex( initListComp , inputlist )

    tests whether test( inputlist ) returns True, and thus whether the symmetry defined in it is true.
    If not, it returns False.
    If yes, it copies the time points in initListComp ( NOT in the format of syminput, just a list of points
    in time ) using the operatorlist in inputlist ( check syminput() documentation ).

    For example, if initListComp is the list of maxima, it will keep applying the operatorlist so long as the
    initListComp is growing. When it reaches closure, it returns the new, expanded initListComp, now having the maxima
    that were previously there and all those reachable via the operators.

    this is NOT guaranteed to give you all the maxima/minima/zero-crossings/window centers of the field.

    -------------
    Example:  expand( extrema_locs , invert( translate( cycle_period / 2 , syminput( timespace ) ) ) ) tests for
    half-cycle symmetry across timespace, and if it finds it, it takes all the time points in extrema_locs
    ( presumably all the extrema locations from 0 to cycle_period ) and uses the half-cycle symmetry to find
    more extrema if possible ( by translating by cycle_period / 2 ).
    -------------------------------------------------------------------------------
    """
    if test( inputlist ) == False:
        print("!!!  Incorrect Symmetry! test returns False")
        return False
    operatorlist = inputlist[ 1 ]

    working_initList = []
    for i in initListComp:
        working_initList.append( [ np.real( i ) , np.imag( i ) ] )

    tlist_modified = []
    for i in working_initList:
        tlist_modified.append( [ 1 , i[ 0 ] , 0 , 0 , i[ 1 ] ] )

    shouldthiscodecontinue = True
    continue_counter = 0
    while shouldthiscodecontinue:  # This while loop ensures we keep applying the operators until closure
        previousLength = len( working_initList )

        tlist_modified = _ApplySymmetryOperatorsComp( tlist_modified , operatorlist , False )
        if tlist_modified == False:  # this happens if the number of reflections exceeds the limit (default: 1000).
            assert False

        for i in tlist_modified:
            if all( min( ( j[ 0 ] - i[ 1 ] ) % cycle_period , ( cycle_period - ( j[ 0 ] - i[ 1 ] ) ) % cycle_period ) >
                    sym_tolerance for j in working_initList):
                working_initList.append( [ i[ 1 ] , i[ 4 ] ] )

        if len( working_initList ) == previousLength:
            shouldthiscodecontinue = False
        continue_counter +=1
        if continue_counter >= 100:
            print("!!! This code should not continue for 100 times over!\nField incommensurate?")
            assert False

    complex_working_initList = []
    for i in working_initList:
        complex_working_initList.append( i[ 0 ] + 1j * i[ 1 ] )
    return complex_working_initList

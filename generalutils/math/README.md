# generalutils.math

    constrain(val, less_lim, more_lim):
        Constrains a value to between provided limits.
    
        :param val: number, value to constrain
        :param more_lim: number, upper constraint
        :param less_lim: number, lower constraint
        :return: number

    rescale(val, in_low, in_high, out_low, out_high, outside='constrain'):
        Rescales val in the input range in_low:in_high to the output range
        out_low:out_high.
    
        If result is outside the output range:
        outside='constrain' : return the value, limited to the range out_low:out_high
        outside='raise' : raise ValueError
        outside='mid' : return middle of output range (average of out_low and out_high)
        outside='ignore' : return result without limiting range
        outside= some value or None : return `outside`
    
        :param val: number, value to rescale to new range
        :param in_low: number, low end of input range
        :param in_high: number, high end of input range
        :param out_low: number, low end of output range
        :param out_high: number, high end of output range
        :param outside: any, see notes above
        :return: any, rescaled value or some provided object, see notes above

    deadband(val, deadband, center=0.0, lower_deadband=None, smooth=False):
        Applies a deadband to `val` about `center`. If `lower_deadband` is not provided,
        `deadband` is considered a magnitude around `center`.
    
        If `val` falls inside of deadband around `default`, returns `center`, otherwise returns `val`.
    
        :param val: number, value on which to ignore values within deadband
        :param deadband: positive number, range of values above `default` to ignore
        :param lower_deadband: positive number, range of values below `default` to ignore
        :param center: number, about which to apply deadband
        :param smooth: bool, whether to recalculate values for a smooth transition out of deadband zone
        :return: number, deadband filtered `val`

    tuple_distance(x, y)
        Calculate euclidean distance between two tuples. Tuple lengths must match.

        :param X: (#, #, ..., #)
        :param Y: (#, #, ..., #)
        :return: float, sum of distances between each pair of elements


### generalutils.math.DESolver
Extension of class version of [scipy.optimize.differential_evolution](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.differential_evolution.html) that can be saved and reloaded.

Also see: scipy.optimize._differentialevolution.DifferentialEvolutionSolver

DESolver_Pbar is the same class with progress bars.

    from differential_evolver import DESolver
    import json
    
    # Make the object
    des = DESolver(func, bounds, ...)
    
    # Save the object's state to a file
    json.dump(des.state, open(file, 'w'))
    
    # Load an object from a file
    reloaded = DESolver(func, args, **json.loads(open(file, 'r')))
    
    # Save the object's state in memory
    backup = des.state.copy()
    
    # Continue solving/iterating as usual
    x, y = next(des)
    # or
    des.solve()

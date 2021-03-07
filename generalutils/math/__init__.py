from scipy.optimize._differentialevolution import DifferentialEvolutionSolver
from math import ceil
import numpy as np
from tqdm import tqdm


def constrain(val, less_lim, more_lim):
    """Constrains a value to between provided limits.

    :param val: number, value to constrain
    :param more_lim: number, upper constraint
    :param less_lim: number, lower constraint
    :return: number
    """
    if val < less_lim:
        return less_lim
    elif val > more_lim:
        return more_lim
    else:
        return val


def rescale(val, in_low, in_high, out_low, out_high, outside='constrain'):
    """Rescales val in the input range in_low:in_high to the output range
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
    """
    # calculate new value
    _ret = ((val - in_low) / (in_high - in_low)) * (out_high - out_low) + out_low

    # _ret is outside output range
    if _ret < out_low or _ret > out_high:
        # apply setting
        if isinstance(outside, str):
            if outside == 'constrain':
                return constrain(_ret, out_low, out_high)
            elif outside == 'mid':
                return (out_high + out_low) / 2  # return middle value
            elif outside == 'ignore':
                return _ret
            elif outside == 'raise':
                raise (
                    ValueError('Rescaling {} in {}:{} falls outside {}:{}'.format(
                        val, in_low, in_high, out_low, out_high)))
            else:
                raise ValueError(f"String `{outside}` is not recognized.")
        else:  # value provided
            return outside  # return provided 'outside' value

    # _ret is inside output range
    return _ret


def deadband(val, deadband, center=0.0, lower_deadband=None, smooth=False):
    """Applies a deadband to `val` about `center`. If `lower_deadband` is not provided,
    `deadband` is considered a magnitude around `center`.

    If `val` falls inside of deadband around `default`, returns `center`, otherwise returns `val`.

    :param val: number, value on which to ignore values within deadband
    :param deadband: positive number, range of values above `default` to ignore
    :param lower_deadband: positive number, range of values below `default` to ignore
    :param center: number, about which to apply deadband
    :param smooth: bool, whether to recalculate values for a smooth transition out of deadband zone
    :return: number, deadband filtered `val`
    """
    if lower_deadband is None:
        # take deadband as magnitude either direction
        lower_deadband = deadband

    if (center - lower_deadband) < val < (center + deadband):
        # value falls within deadband
        return center
    else:
        if smooth is True:
            if val > center:
                val -= deadband
            elif val < center:
                val += lower_deadband
            else:
                raise NotImplementedError("This should never occur")
        return val


def tuple_distance(X, Y):
    """Calculate euclidean distance between two tuples. Tuple lengths must match.

    :param X: (#, #, ..., #)
    :param Y: (#, #, ..., #)
    :return: float, sum of distances between each pair of elements
    """
    from math import sqrt

    if len(X) != len(Y):
        raise TypeError(f"Tuple lengths are unequal: {len(X)}!={len(Y)}")

    sum = 0
    for i in range(len(X)):
        sum += (X[i] - Y[i]) ** 2
    return sqrt(sum)


# def intersect_segment_circle(start, end, circle, fudge=0.0):
#     """
#     Test whether a line segment and circle intersect.
#     :param Entity start: The start of the line segment. (Needs X, Y attributes)
#     :param Entity end: The end of the line segment. (Needs X, Y attributes)
#     :param Entity circle: The circle to test against. (Needs X, Y, r attributes)
#     :param float fudge: A fudge factor; additional distance to leave between the segment and circle.
#     :return: True if intersects, False otherwise
#     :rtype: bool
#     """
#     # Derived with SymPy
#     # Parameterize the segment as start + t * (end - start),
#     # and substitute into the equation of a circle
#     # Solve for t
#     dx = end.X - start.X
#     dy = end.Y - start.Y
#
#     a = dx**2 + dy**2
#     b = -2 * (start.X**2 - start.X*end.X - start.X*circle.X + end.X*circle.X +
#               start.Y**2 - start.Y*end.Y - start.Y*circle.Y + end.Y*circle.Y)
#     c = (start.X - circle.X)**2 + (start.Y - circle.Y)**2
#
#     if a == 0.0:
#         # Start and end are the same point
#         return start.calculate_distance_between(circle) <= (circle.radius + fudge) ** 2
#
#     # Time along segment when closest to the circle (vertex of the quadratic)
#     t = min(-b / (2 * a), 1.0)
#     if t < 0:
#         return False
#
#     closest_x = start.X + dx * t
#     closest_y = start.Y + dy * t
#     closest_distance = Position(closest_x, closest_y).calculate_distance_between(circle)
#
#     return closest_distance <= (circle.radius + fudge) ** 2

# From MATLAB Project
# %% IntersectPipe.m
# % Tim Olson - timjolson@user.noreplay.github.com
# %
# % Detects intersection of a ray and circle (pipe)
# function [ p ] = IntersectPipe( v1, p1, c, d, show )
# % Pass in vector, it's startpoint, center height of pipe, diameter of pipe,
# % and whether or not to show calculated vectors
# % Returns coordinates of intersection
# % returns [0;-2] if no intersection
#
# % handle things coming in sideways
# if isequal([1,2],size(v1))
#     v1 = v1';
# end
# if isequal([1,2],size(p1))
#     p1 = p1';
# end
#
# % Projection lengths and such
# % http://doswa.com/2009/07/13/circle-segment-intersectioncollision.html
# v1 = v1./norm(v1); % incoming ray, unit vector
# temp = p1 - [0;c]; % vector between pipe center and start of v1
# proj = abs(temp'*v1); % project temp onto v1 = length along v1 at normal distance
# proj = proj*v1; % move along v1 by length proj
# pp = proj + p1; % projected point = previous vector + startpoint of v1
# perp = -pp + [0;c]; % vector from pipe center to projected point
# len = norm(perp); % length of perp
#
# if show
#     % Plot perpendicular vector
#     PlotVector(perp,pp,'k-.');
#     % Plot projection point
#     plot(pp(1),pp(2),'ko');
# end
#
# % Check for intersection
# % perpendicular vector length less than radius
# if len < d/2
#     p = pp;
# else
#     % return failure info
#     p = [0;-2];
# end
# end


class DESolver(DifferentialEvolutionSolver):
    __doc__ = str(DifferentialEvolutionSolver.__doc__) + \
              """
              Custom:
              state - kwargs dict to resume with DESolver(func, **state)
              X - copy of population
              Y - copy of function results (ordered same as population)
              y - best result (lowest energy)
              
              gen_callback(DESolver)
              feval_callback(DESolver, x, y, *args)
              
              """

    def __init__(self, func, bounds, args=(), **kwargs):
        # store standard things
        self.seed = kwargs.get('seed', None)
        self.workers = kwargs.get('workers', 1)

        # change `polish` default to False
        kwargs.setdefault('polish', False)

        # store things needed to continue from a saved state (that don't pass to original class)
        nrg = kwargs.pop('nrg', None)
        nfev = kwargs.pop('nfev', 0)
        constraint_violation = kwargs.pop('constraint_violation', None)
        feasible = kwargs.pop('feasible', None)

        def _func(parameters, *args):
            rv = func(parameters, *args)
            if self._nfev <= self.num_population_members:
                self._nfev += 1     # nfev does not get updated during initial population eval
            self.feval_callback(self, parameters, rv, *args)
            return rv

        super().__init__(_func, bounds, args, **kwargs)

        if nrg is not None:
            self.population_energies[:] = nrg[:]

        self._nfev = nfev or 0
        self._inited = nfev >= self.num_population_members

        if constraint_violation is not None:
            self.constraint_violation = np.asarray(constraint_violation)
        if feasible is not None:
            self.feasible = np.asarray(feasible)

    def feval_callback(self, parameters, rv, *args):
        return None

    def gen_callback(self):
        return None

    def _calculate_population_energies(self, population):
        rv = super()._calculate_population_energies(population)
        if self._inited is False:
            # must subtract eval count, since we manually count up inside function
            self._nfev -= self.num_population_members
            self._inited = True
        return rv

    def __next__(self):
        __doc__ = DifferentialEvolutionSolver.__next__.__doc__ + "\nCustom:\nAdditionally calls gen_callback()"
        x, nrg = DifferentialEvolutionSolver.__next__(self)
        self.gen_callback()
        return x, nrg

    @property
    def state(self):
        return dict(
            nfev=self._nfev,
            popsize=int(self.num_population_members / self.parameter_count),
            bounds=self.limits.T.tolist(),
            maxiter=self.maxiter,
            maxfun=self.maxfun,
            mutation=list(self.scale) if hasattr(self.scale, '__iter__') else self.scale,
            recombination=self.cross_over_probability,
            tol=self.tol,
            atol=self.atol,
            strategy=self.strategy,
            seed=self.seed,
            polish=bool(self.polish),
            disp=bool(self.disp),
            updating=self._updating,
            workers=self.workers,
            init=self.X.tolist(),
            nrg=self.population_energies.T.tolist(),
            constraints=list(self.constraints),
            constraint_violation=self.constraint_violation.tolist() if isinstance(self.constraint_violation, np.ndarray) \
                else self.constraint_violation,
            feasible=list(map(bool, self.feasible))
        ).copy()

    @property
    def X(self):
        """The current population without internal scaling"""
        return self._scale_parameters(self.population)

    @property
    def Y(self):
        """The current population energies"""
        return self.population_energies.copy()

    @property
    def y(self):
        """The current best energy"""
        return self.population_energies[0]


class DESolver_Pbar(DESolver):
    def __init__(self, func, bounds, args=(), **kwargs):
        # wrap func with pbar updates
        def _func(parameters, *args):
            rv = func(parameters, *args)
            self.pbar_feval.update()
            self.pbar_gen_mutations.update()
            self.pbar_gens.update(1 / self.num_population_members)
            return rv

        super().__init__(_func, bounds, args, **kwargs)

        if not np.isfinite(self.maxfun):  # no max fun
            if not np.isfinite(self.maxiter):  # no max fun, no max iter/gen
                maxfeval = np.inf
            else:  # no max fun, max iter/gen
                self.maxfun = maxfeval = (self.maxiter + 1) * self.num_population_members
                self.maxiter = ceil(maxfeval / self.num_population_members)
        else:  # max fun
            if not np.isfinite(self.maxiter):  # max fun, no max iter/gen
                maxfeval = self.maxfun
            else:  # max fun, max iter/gen
                i = (self.maxiter + 1) * self.num_population_members  # by generations
                if i < self.maxfun:  # dictated by iter
                    self.maxfun = maxfeval = i
                    self.maxiter = ceil(self.maxfun / self.num_population_members)
                elif self.maxfun < i:  # dictated by fun
                    maxfeval = self.maxfun
                    self.maxiter = ceil(self.maxfun / self.num_population_members)
                else:
                    maxfeval = self.maxfun

        mut_total = self.num_population_members
        gen_initial = self._nfev / mut_total
        mut_initial = (self._nfev % mut_total)

        self.pbar_feval = tqdm(
            initial=self._nfev, total=maxfeval if np.isfinite(maxfeval) else 0,
            leave=True, ncols=80, desc='F-Evals',
            bar_format='{desc}: {percentage:.2f}%|{bar}| {n}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]')
        self.pbar_gens = tqdm(
            initial=gen_initial, total=self.maxiter,
            leave=True, ncols=80, desc='Generation',
            bar_format='{desc}: {percentage:.2f}%|{bar}| {n:.2f}/{total_fmt} [{rate_fmt}{postfix}]')
        self.pbar_gen_mutations = tqdm(
            initial=mut_initial, total=mut_total,
            leave=False, ncols=80, desc='Mutation',
            bar_format='{desc}: {percentage:.2f}%|{bar}| {n}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]')

    def __next__(self):
        self.pbar_gen_mutations.close()
        self.pbar_gen_mutations = tqdm(
            total=self.num_population_members,
            leave=False, ncols=80, desc='Mutation',
            bar_format='{desc}: {percentage:.2f}%|{bar}| {n}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]')

        try:
            x, nrg = DifferentialEvolutionSolver.__next__(self)
        except StopIteration as e:
            self._promote_lowest_energy()
            self.gen_callback()
            raise

        self.gen_callback()
        return self.x, self.y

    def solve(self):
        res = super().solve()
        self.pbar_feval.close()
        self.pbar_gens.close()
        self.pbar_gen_mutations.close()
        return res


__all__ = ['constrain', 'rescale', 'deadband', 'tuple_distance']

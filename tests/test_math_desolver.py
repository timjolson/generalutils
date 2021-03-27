import pytest
import os, sys, logging, json
from scipy.optimize import rosen
import numpy as np
import time

from generalutils.math import DESolver, DESolver_Pbar

logging.basicConfig(filename='logs/test_math_desolver.log', filemode='w', level=logging.DEBUG)


def clear_file(filename):
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass


def test_state():
    # make state
    des = DESolver(rosen, bounds=[(0, 2)] * 5)
    backup = des.state.copy()

    # make from state
    from_state = DESolver(rosen, **backup)

    # verify matching state (state includes population, energies, config options, etc.)
    assert des.state == from_state.state


def test_from_state_file():
    filename = "logs/desolver_from_state_file"
    clear_file(filename)

    # make file
    des = DESolver(rosen, bounds=[(0, 2)] * 5, popsize=12)
    json.dump(des.state, open(filename, 'w'), indent=4)

    # make from file
    from_state = DESolver(rosen, **json.load(open(filename, 'r')))

    # verify matching state (state includes population, energies, config options, etc.)
    assert des.state == from_state.state

    # This fails regularly, appears to be low level, inconsequential math error
    # Any differences between arrays should be extremely small (float error, etc.)
    assert np.allclose(des.population, from_state.population)
    logging.debug(f"diff\n{des.population - from_state.population}")

    res = from_state.solve()
    logging.debug(f"solution=\n{res}")
    # Make sure func can be solved when made from_state
    assert np.isclose(res.x, 1.0).all()
    assert np.isclose(res.fun, 0.0)

    # cleanup
    clear_file(filename)


def test_iterate_load_save():
    filename = 'logs/desolver_iterate_load_save'
    clear_file(filename)

    # iterate solver
    iters = 15
    popsize = 18

    # make file
    des = DESolver(rosen, bounds=[(0, 2)] * 5, popsize=popsize)
    json.dump(des.state, open(filename, 'w'))

    # load file
    des = DESolver(rosen, **json.load(open(filename, 'r')))

    # iterate some
    for i in range(iters):
        x, y = next(des)
        logging.debug(f"nfev:{des._nfev}  iteration/generation: {i} \tx:{x}\ty:{y}")
    assert des._nfev == (iters + 1) * popsize * des.parameter_count + 1
    assert des._nfev == (iters + 1) * des.num_population_members + 1
    des_state_backup = des.state

    # reload file
    del des
    des = DESolver(rosen, **des_state_backup)
    assert des._nfev == (iters + 1) * popsize * des.parameter_count + 1
    assert des._nfev == (iters + 1) * des.num_population_members + 1
    # solve
    assert np.isclose(des.solve().x, 1.0).all()

    # cleanup
    clear_file(filename)


def test_tqdm_maxfun_maxiter():
    des = DESolver_Pbar(lambda x: [rosen(x), time.sleep(.001)][0],
                   bounds=[(0, 2)] * 5,
                   popsize=2, maxiter=4, maxfun=30)
    des.solve()
    assert des.num_population_members == 10
    assert des._nfev == 31
    assert des.pbar_feval.n == 30
    assert des.pbar_gen_mutations.n == 0
    assert np.isclose(des.pbar_gens.n, 3.0)


def test_tqdm_maxfun_maxiter_2():
    des = DESolver_Pbar(lambda x: [rosen(x), time.sleep(.001)][0],
                   bounds=[(0, 2)] * 5,
                   popsize=2, maxiter=4, maxfun=31)
    des.solve()
    assert des.num_population_members == 10
    assert des._nfev == 32
    assert des.pbar_feval.n == 31
    assert des.pbar_gen_mutations.n == 1
    assert np.isclose(des.pbar_gens.n, 3.1)


def test_tqdm_maxiter_maxfun():
    des = DESolver_Pbar(lambda x: [rosen(x), time.sleep(.1)][0],
                   bounds=[(0, 2), (0, 2), (0, 2), (0, 2), (0, 2)],
                   popsize=2, maxiter=1, maxfun=30)
    des.solve()
    assert des.pbar_feval.n == 20
    assert des.pbar_gen_mutations.n == 0
    assert np.isclose(des.pbar_gens.n, 2.0)


def test_tqdm_maxiter_maxfun_0():
    des = DESolver_Pbar(lambda x: [rosen(x), time.sleep(.1)][0],
                   bounds=[(0, 2), (0, 2), (0, 2), (0, 2), (0, 2)],
                   popsize=2, maxiter=0, maxfun=30)
    des.solve()
    assert des.pbar_feval.n == 10
    assert des.pbar_gen_mutations.n == 10
    assert np.isclose(des.pbar_gens.n, 1.0)


def test_tqdm_maxiter():
    des = DESolver_Pbar(lambda x: [rosen(x), time.sleep(.1)][0],
                   bounds=[(0, 2), (0, 2), (0, 2), (0, 2), (0, 2)],
                   popsize=2, maxiter=2)
    des.solve()
    assert des.pbar_feval.n == 30
    assert des.pbar_gen_mutations.n == 0
    assert np.isclose(des.pbar_gens.n, 3.0)


def test_tqdm_maxfun():
    des = DESolver_Pbar(lambda x: [rosen(x), time.sleep(.1)][0],
                   bounds=[(0, 2), (0, 2), (0, 2), (0, 2), (0, 2)],
                   popsize=2, maxfun=23)
    des.solve()
    assert des.pbar_feval.n == 23
    assert des.pbar_gen_mutations.n == 3
    assert np.isclose(des.pbar_gens.n, 2.3)


def test_tqdm_maxiter_short():
    des = DESolver_Pbar(lambda x: [rosen(x), time.sleep(.1)][0],
                   bounds=[(0, 2), (0, 2), (0, 2), (0, 2), (0, 2)],
                   popsize=2, maxiter=1)
    des.solve()
    assert des.pbar_feval.n == 20
    assert des.pbar_gen_mutations.n == 0
    assert np.isclose(des.pbar_gens.n, 2.0)


def test_tqdm_resume():
    des = DESolver_Pbar(lambda x: [rosen(x), time.sleep(.1)][0],
                   bounds=[(0, 2)] * 5,
                   popsize=2, maxiter=1)
    des.solve()
    assert des.pbar_feval.n == 20
    assert des.pbar_gen_mutations.n == 0
    assert np.isclose(des.pbar_gens.n, 2.0)

    des = DESolver_Pbar(rosen, **des.state)
    assert des._nfev == 21
    assert des.pbar_feval.n == 21
    assert des.pbar_gen_mutations.n == 1
    assert des.pbar_gens.n == 2.1

    try:
        x, y = next(des)
    except StopIteration:
        pass

    assert des._nfev == 21
    assert des.pbar_feval.n == 21
    assert des.pbar_gen_mutations.n == 0
    assert np.isclose(des.pbar_gens.n, 2.1)

    state = des.state.copy()
    state.update(maxfun=30)
    des = DESolver_Pbar(rosen, **state)

    x, y = next(des)
    assert des._nfev == 31
    assert des.pbar_feval.n == 31
    assert des.pbar_gen_mutations.n == 10
    assert np.isclose(des.pbar_gens.n, 3.1)


def test_tqdm_resume_interrupted():
    des = DESolver_Pbar(lambda x: [rosen(x), time.sleep(.1)][0],
                   bounds=[(0, 2)] * 5,
                   popsize=2, maxfun=23)
    des.solve()
    assert des.pbar_feval.n == 23
    assert des.pbar_gen_mutations.n == 3
    assert np.isclose(des.pbar_gens.n, 2.3)

    state = des.state.copy()
    state['maxfun'] = 40
    des = DESolver_Pbar(rosen, **state)
    assert des._nfev == 24
    assert des.pbar_feval.n == 24
    assert des.pbar_gen_mutations.n == 4
    assert np.isclose(des.pbar_gens.n, 2.4)

    # should finish the generation?
    x, y = next(des)
    assert des._nfev == 34
    assert des.pbar_feval.n == 34
    assert des.pbar_gen_mutations.n == 10
    assert np.isclose(des.pbar_gens.n, 3.4)

    with pytest.raises(StopIteration):
        x, y = next(des)
    assert des._nfev == 41
    assert des.pbar_feval.n == 41
    assert des.pbar_gen_mutations.n == 7
    assert np.isclose(des.pbar_gens.n, 4.1)


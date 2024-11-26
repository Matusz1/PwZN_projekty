import argparse
import numpy as np
import scipy as sp
import numba
import time
from PIL import Image, ImageDraw

parser = argparse.ArgumentParser()
parser.add_argument('--size', '-s', type=int, default=10, help='Size of ising model (s*s)')
parser.add_argument('-J', type=float, default=1, help='Coupling constant')
parser.add_argument('-B', type=float, default=0, help='External magnetic field')
parser.add_argument('--beta', '-b', type=float, default=1, help='Inverse temperature')
parser.add_argument('--n-steps', '-n', type=int, default=10, help='Number of makrosteps')
parser.add_argument('--spin-density', '-d', type=float, default=0.5, help='Initial spin density')
parser.add_argument('--image_prefix', '-i', help='Prefix for image files')
parser.add_argument('--animation_prefix', '-a', help='Prefix for animation files')
parser.add_argument('--magnetization_prefix', '-m', help='Prefix for magnetization files')

args = parser.parse_args()

@numba.njit
def get_energy(spins, J, B):
    return -0.5 * J * np.sum(sp.signal.convolve2d(spins, np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]), mode='same')) - B * np.sum(spins)

@numba.njit
def next_step(spins, J, B, beta):
    next_spins = np.copy(spins)
    size = spins.shape[0]
    for _ in range(size**2):
        i = np.random.randint(size)
        j = np.random.randint(size)
        # Find the change in energy with non-periodic boundary conditions
        dE = 0
        c = spins[i, j]
        if i > 0:
            dE += c * spins[i-1, j]
        if i < size-1:
            dE += c * spins[i+1, j]
        if j > 0:
            dE += c * spins[i, j-1]
        if j < size-1:
            dE += c * spins[i, j+1]
        dE *= 2 * J
        dE += 2 * B * c
        if dE < 0 or np.random.rand() < np.exp(-beta * dE):
            next_spins[i, j] *= -1
    return next_spins

def save_images(spins_list, image_prefix):
    for i, spins in enumerate(spins_list):
        size = spins.shape[0]
        image = Image.new('RGB', (size*10, size*10), 'white')
        draw = ImageDraw.Draw(image)
        for i in range(size):
            for j in range(size):
                color = 'orange' if spins[i, j] == 1 else 'blue'
                draw.rectangle([i*10, j*10, (i+1)*10, (j+1)*10], fill=color)
        image.save(image_prefix + str(i) + '.png')

def save_animation(spins_list, animation_prefix):
    frames = []
    for spins in spins_list:
        size = spins.shape[0]
        image = Image.new('RGB', (size*10, size*10), 'white')
        draw = ImageDraw.Draw(image)
        for i in range(size):
            for j in range(size):
                color = 'orange' if spins[i, j] == 1 else 'blue'
                draw.rectangle([i*10, j*10, (i+1)*10, (j+1)*10], fill=color)
        frames.append(image)
    frames[0].save(animation_prefix + '.gif', save_all=True, append_images=frames[1:], duration=100, loop=0)

@numba.njit
def calc_magnetization(spins):
    size = spins.shape[0]
    return np.sum(spins) / size**2

def save_magnetization(spins_list, magnetization_prefix):
    magnetizations = np.array([calc_magnetization(spins) for spins in spins_list])
    with open(magnetization_prefix + '.txt', 'w') as f:
        f.write('# step magnetization\n')
        for step, magnetization in enumerate(magnetizations):
            f.write(f'{step} {magnetization}\n')


@numba.njit
def run_simulation(
        n_steps,
        size,
        J,
        B,
        beta,
        spin_density,
    ):
    initial_spins = np.zeros((size, size), dtype=np.int8)
    for i in range(size):
        for j in range(size):
            initial_spins[i, j] = 1 if np.random.rand() < spin_density else -1

    spins = [initial_spins]
    for _ in range(n_steps):
        spins.append(next_step(spins[-1], J, B, beta))

    return spins

run_simulation(
    n_steps=1,
    size=args.size,
    J=args.J,
    B=args.B,
    beta=args.beta,
    spin_density=args.spin_density,
)

beg = time.time()
spins_list = run_simulation(
    n_steps=args.n_steps,
    size=args.size,
    J=args.J,
    B=args.B,
    beta=args.beta,
    spin_density=args.spin_density,
)
print('Elapsed time:', time.time() - beg)

if args.image_prefix:
    save_images(spins_list, args.image_prefix)
if args.animation_prefix:
    save_animation(spins_list, args.animation_prefix)
if args.magnetization_prefix:
    save_magnetization(spins_list, args.magnetization_prefix)

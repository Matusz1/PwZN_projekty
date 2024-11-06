import argparse
import numpy as np
import scipy as sp
import tqdm
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

class IsingModel:
    cell_pixels = 10
    def __init__(self, size, J, B, beta, spin_density):
        self.size = size
        self.J = J
        self.B = B
        self.beta = beta
        self.spins = np.random.choice([-1, 1], size=(size, size), p=[1-spin_density, spin_density])
        
    def get_energy(self):
        return -0.5 * self.J * np.sum(sp.signal.convolve2d(self.spins, np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]), mode='same')) - self.B * np.sum(self.spins)
    
    def get_magnetization(self):
        return np.sum(self.spins) / self.size**2
    
    def update(self):
        for _ in range(self.size**2):
            i = np.random.randint(self.size)
            j = np.random.randint(self.size)
            # Find the change in energy with non-periodic boundary conditions
            dE = 0
            c = self.spins[i, j]
            if i > 0:
                dE += c * self.spins[i-1, j]
            if i < self.size-1:
                dE += c * self.spins[i+1, j]
            if j > 0:
                dE += c * self.spins[i, j-1]
            if j < self.size-1:
                dE += c * self.spins[i, j+1]
            dE *= 2 * self.J
            dE += 2 * self.B * c
            if dE < 0 or np.random.rand() < np.exp(-self.beta * dE):
                self.spins[i, j] *= -1

    def get_image(self):
        image = Image.new('RGB', (self.size*self.cell_pixels, self.size*self.cell_pixels), 'white')
        draw = ImageDraw.Draw(image)
        for i in range(self.size):
            for j in range(self.size):
                color = 'orange' if self.spins[i, j] == 1 else 'blue'
                draw.rectangle([i*self.cell_pixels, j*self.cell_pixels, (i+1)*self.cell_pixels, (j+1)*self.cell_pixels], fill=color)
        return image

    def run_simulation(self, n_steps, image_prefix=None, animation_prefix=None, magnetization_prefix=None):
        frames = []
        magnetizations = []
        if image_prefix or animation_prefix:
            image = self.get_image()
            frames.append(image)
            if image_prefix:
                image.save(image_prefix + '0.png')
        if magnetization_prefix:
            magnetizations.append([0, self.get_magnetization()])
        for step in tqdm.tqdm(range(1, n_steps+1)):
            self.update()
            if image_prefix or animation_prefix:
                image = self.get_image()
                frames.append(image)
                if image_prefix:
                    image.save(image_prefix + str(step) + '.png')
            if magnetization_prefix:
                magnetizations.append([step, self.get_magnetization()])
        if animation_prefix:
            print('Saving animation...')
            frames[0].save(animation_prefix + '.gif', save_all=True, append_images=frames[1:], duration=100, loop=0)
        if magnetization_prefix:
            with open(magnetization_prefix + '.txt', 'w') as f:
                f.write('# step magnetization\n')
                for step, magnetization in magnetizations:
                    f.write(f'{step} {magnetization}\n')

model = IsingModel(args.size, args.J, args.B, args.beta, args.spin_density)
model.run_simulation(args.n_steps, args.image_prefix, args.animation_prefix, args.magnetization_prefix)

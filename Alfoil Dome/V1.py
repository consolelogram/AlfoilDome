import numpy as np
import matplotlib.pyplot as plt

dt = 0.1
steps = 1000
hit_radius = 0.1

def normalize(v):
    n = np.linalg.norm(v)
    if n > 0:
        return v / n 
    else:
        return v

class Rocket:
    def __init__(self):
        # random starting position (3D)
        self.pos = np.random.uniform(-100, 100, size=3)

        # random direction in 3D
        direction = normalize(np.random.randn(3))
        self.pos = np.array([50, -30, 20], dtype=float)


        # random speed (scalar)
        speed = np.random.uniform(2, 4)

        # velocity = direction × speed
        self.vel = direction * speed

    def step(self):
        self.pos += self.vel * dt
        return self.pos

class Catcher:
    def __init__(self):
        self.pos = np.array([0.0, 0.0, 0.0])
        self.speed = 3

    def step(self, observed_pos):
        direction = normalize(observed_pos - self.pos)
        self.pos += direction * self.speed * dt
        return self.pos


rocket = Rocket()
catcher = Catcher()

rocket_path = []
catcher_path = []

from matplotlib.animation import FuncAnimation

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)
ax.set_zlim(-100, 100)

rocket_line, = ax.plot([], [], [], color="blue", label="Rocket")
catcher_line, = ax.plot([], [], [], color="orange", label="Catcher")
ax.scatter(0, 0, 0, color='orange', s=40)
ax.legend()

rocket_path = []
catcher_path = []

def update(frame):
    for _ in range(5):   # try 5–10
        r_pos = rocket.step()
        c_pos = catcher.step(r_pos)
        rocket_path.append(r_pos.copy())
        catcher_path.append(c_pos.copy())
        if np.linalg.norm(r_pos - c_pos) < hit_radius:
            ani.event_source.stop()
            ax.scatter(c_pos[0], c_pos[1], c_pos[2], color='red', s=50)
            break

    rp = np.array(rocket_path)
    cp = np.array(catcher_path)

    rocket_line.set_data(rp[:,0], rp[:,1])
    rocket_line.set_3d_properties(rp[:,2])

    catcher_line.set_data(cp[:,0], cp[:,1])
    catcher_line.set_3d_properties(cp[:,2])

    return rocket_line, catcher_line

ani = FuncAnimation(fig, update, frames=steps, interval=1, blit=False)
plt.show()

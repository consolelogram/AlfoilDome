import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

dt = 0.05
steps = 1000
hit_radius = 0.1
np.random.seed(None)
BOUND = 150
reset_pending = False

def normalize(v):  # unit vector
    n = np.linalg.norm(v)
    if n > 0:
        return v / n 
    else:
        return v

class Rocket:
    def __init__(self):
        rng = np.random.default_rng()

        self.pos = rng.uniform(-100, 100, size=3)
        direction = normalize(rng.standard_normal(3))
        speed = rng.uniform(2, 5)

        self.vel = direction * speed
        self.amax = 2   
        self.rng = rng

    def step(self):
        accel = normalize(self.rng.standard_normal(3)) * self.amax

        self.vel += accel * dt # euler's
        self.pos += self.vel * dt

        return self.pos


class Catcher:
    def __init__(self):
        self.pos = np.array([0.0, 0.0, 0.0])
        self.vel = np.zeros(3)
        self.vmax = 6.0
        self.amax = 10.0

    def step(self, rocket_pos):
        r = rocket_pos - self.pos
        direction = normalize(r)

        # desired velocity toward target
        v_des = direction * self.vmax

        # acceleration tries to correct velocity error
        accel = v_des - self.vel

        # cap acceleration
        a_norm = np.linalg.norm(accel)
        if a_norm > self.amax:
            accel = accel / a_norm * self.amax

        # integrate
        self.vel += accel * dt
        self.pos += self.vel * dt

        return self.pos


rocket = Rocket()
catcher = Catcher()

rocket_path = []
catcher_path = []

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)
ax.set_zlim(-100, 100)

info_text = ax.text2D(
    0.02, 0.95, "",
    transform=ax.transAxes
)
info_text.set_bbox(dict(facecolor='white', alpha=0.6, edgecolor='none'))

rocket_line, = ax.plot([], [], [], color="blue", label="Rocket")
catcher_line, = ax.plot([], [], [], color="orange", label="Catcher")
ax.scatter(0, 0, 0, color='orange', s=20)
ax.legend()

rocket_path = []
catcher_path = []

def reset_sim():
    global rocket, catcher
    rocket = Rocket()
    catcher = Catcher()

    rocket_path.clear()
    catcher_path.clear()

    rocket_path.append(rocket.pos.copy())
    catcher_path.append(catcher.pos.copy())
    global hit_marker
    if hit_marker is not None:
        hit_marker.remove()
        hit_marker = None


hit_marker = None

def out_of_bounds(pos):
    return np.any(np.abs(pos) > BOUND)


def update(frame):
    for _ in range(5):   # try 5–10
        r_pos = rocket.step()
        c_pos = catcher.step(r_pos)
        rocket_path.append(r_pos.copy())
        catcher_path.append(c_pos.copy())
        
        if np.linalg.norm(r_pos - c_pos) < hit_radius:
            reset_sim()
            global hit_marker
            hit_marker = ax.scatter(c_pos[0], c_pos[1], c_pos[2], color='red', s=50)
            reset_pending = True
            break

        if out_of_bounds(r_pos) or out_of_bounds(c_pos):
            reset_sim()
            return rocket_line, catcher_line

    rp = np.array(rocket_path)
    cp = np.array(catcher_path)

    rocket_line.set_data(rp[:,0], rp[:,1])
    rocket_line.set_3d_properties(rp[:,2])

    catcher_line.set_data(cp[:,0], cp[:,1])
    catcher_line.set_3d_properties(cp[:,2])

    rel = r_pos - c_pos

    info_text.set_text(
        f"Rocket pos: {r_pos.round(2)}\n"
        f"Catcher pos: {c_pos.round(2)}\n"
        f"Relative: {rel.round(2)}"
    )


    return rocket_line, catcher_line

ani = FuncAnimation(fig, update, frames=steps, interval=1, blit=False)
plt.show()




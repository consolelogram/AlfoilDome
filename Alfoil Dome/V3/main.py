import pybullet as p
import pybullet_data
import time

# connect (DIRECT first, GUI later)
cid = p.connect(p.GUI)

# basic setup
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.setTimeStep(1/240)

# ground
plane_id = p.loadURDF("plane.urdf")

# test object (this replaces your old "rocket" placeholder)
sphere_radius = 0.2
mass = 1.0

collision = p.createCollisionShape(
    shapeType=p.GEOM_SPHERE,
    radius=sphere_radius
)

visual = p.createVisualShape(
    shapeType=p.GEOM_SPHERE,
    radius=sphere_radius,
    rgbaColor=[1, 0, 0, 1]
)

sphere_id = p.createMultiBody(
    baseMass=mass,
    baseCollisionShapeIndex=collision,
    baseVisualShapeIndex=visual,
    basePosition=[0, 0, 5]
)

# set initial velocity AFTER creation
p.resetBaseVelocity(
    sphere_id,
    linearVelocity=[2, 0, 0],
    angularVelocity=[0, 0, 0]
)


# simulate
for i in range(240):
    p.stepSimulation()
    pos, orn = p.getBasePositionAndOrientation(sphere_id)
    vel, ang = p.getBaseVelocity(sphere_id)
    time.sleep(1/240)
    #print(f"t={i/240:.2f}s pos={pos} vel={vel}")


p.disconnect()

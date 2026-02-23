# 3D Kinematic Pursuit Simulation

A 3D simulation of an autonomous tracking agent (Catcher) intercepting an erratically moving target (Rocket) using constrained kinematics and numerical integration.

## Physics & Control Mechanics

### Numerical Integration

The simulation operates on discrete time steps ().

It uses Forward Euler integration to update the velocity () and position () of both bodies:


### The Interceptor (Catcher) Dynamics

The Catcher uses a velocity-matching pure pursuit algorithm.

* **Displacement:** Calculates the line-of-sight vector to the target: .
* **Desired Velocity:** Determines the optimal vector pointing directly at the target: .
* **Acceleration:** Computes the thrust needed to correct its current trajectory: .
* **Constraints:** Acceleration is strictly clamped to . Speed is capped at .

### The Target (Rocket) Dynamics

The Rocket acts as a continuous-thrust evasive body.

It generates a randomized 3D unit vector for its acceleration at each step. This vector is scaled by its physical limit ().

This ensures a smooth, physically continuous flight path rather than discrete, impossible jumps in position.


* **Dependencies:** numpy, matplotlib.
* **Conditions:** Resets upon intercept (distance ) or boundary breach ( units).



This was written with V2 in mind.

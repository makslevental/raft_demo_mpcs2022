# Raft sketch for MPCS-52040-2022

![Alt text](./3spheres.png)

This repo is a sketch of Raft over ZMQ. The commit history follows the process of iterating from a minimal working example (MWE) for ZMQ, to the present sketch.

## The MWE

[c902be1833de2082d633f00fad9f2f7c636bd758](https://github.com/makslevental/raft_demo_mpcs2022/commit/c902be1833de2082d633f00fad9f2f7c636bd758)

Pulled from [SO](https://stackoverflow.com/q/61634119).

## Refactor to work with multiple nodes

[6ae80b40514e92d09372e3fdd459caafedf7d64f](https://github.com/makslevental/raft_demo_mpcs2022/commit/6ae80b40514e92d09372e3fdd459caafedf7d64f)

## Refactor into classes with locks around sockets

[87e2c8080206684be10e3f1738a3bb146d612d36](https://github.com/makslevental/raft_demo_mpcs2022/commit/87e2c8080206684be10e3f1738a3bb146d612d36)

## Add resettable timer

Pulled from [SO](https://stackoverflow.com/a/56169014)

[ad5bf56284f0d66fb4dd025e411192374d06c108](https://github.com/makslevental/raft_demo_mpcs2022/commit/ad5bf56284f0d66fb4dd025e411192374d06c108)

## Refactor into separate files, add logger, and skeleton of Raft node

[bf44d2a4b4b2a0d449ba03500dd24a8ee979ab88](https://github.com/makslevental/raft_demo_mpcs2022/commit/bf44d2a4b4b2a0d449ba03500dd24a8ee979ab88)

## Hookup the timer and ZMQ to the Raft node and check that RPCs can be sent an received

[bb0d3fdf7a972d3b40a84dade0f24f9a1f5394f9](https://github.com/makslevental/raft_demo_mpcs2022/commit/bb0d3fdf7a972d3b40a84dade0f24f9a1f5394f9)

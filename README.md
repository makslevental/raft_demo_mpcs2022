# Raft sketch for MPCS-52040-2022

![Alt text](./3spheres.png)

This repo is a sketch of Raft over Flask. The commit history follows the process of iterating from a minimal working example (MWE), to the present sketch.

## The MWE

[01671b9e8fb147baf765539a4a1817648ed36b48](https://github.com/makslevental/raft_demo_mpcs2022/commit/01671b9e8fb147baf765539a4a1817648ed36b48)

## Refactor to work with multiple nodes

[55781bb0bbedbe7387a9e705ee61c7069ec3415c](https://github.com/makslevental/raft_demo_mpcs2022/commit/55781bb0bbedbe7387a9e705ee61c7069ec3415c)

## Add resettable timer and refactor into separate files, add logger

Pulled from [SO](https://stackoverflow.com/a/56169014)

[b34c869ae6072a1eef6c92aceb88b64ca285bcfd](https://github.com/makslevental/raft_demo_mpcs2022/commit/b34c869ae6072a1eef6c92aceb88b64ca285bcfd)

##  Add skeleton of Raft node

[5912d2b8914b7e6c0fd098d40b83487e7732cda8](https://github.com/makslevental/raft_demo_mpcs2022/commit/5912d2b8914b7e6c0fd098d40b83487e7732cda8)

## Data race example

[72f2e85e854d43271c58dc341414ad8906cd8c6f](https://github.com/makslevental/raft_demo_mpcs2022/commit/72f2e85e854d43271c58dc341414ad8906cd8c6f)

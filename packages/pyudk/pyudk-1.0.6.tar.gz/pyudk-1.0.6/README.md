# pyudk


This library provides Udwadia Kalaba constrained parameters and force quantities for Python 3 out of the box. The usage is mostly based on numpy and sympy library.

## Installation

Just run

    pip install pyudk


## Usage
### Basic usage

The simplest usage would be

    import pyudk as udk
    Qc = udk.ideal_Constraint_force(m, q, A, b)

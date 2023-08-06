# EOPricer Model

This simple Python package calculates the price of some barrier and exotic options.
This consists on an adptation of the Black and Scholes Model to the Bjerksund e Stensland Studies.

## Install
```bash
pip install exotic-options
```
## Import
```python
from exotic_options import EOPricer
```
## Class and Function arguments
Args:
    S (float): Current price of the underlying asset.
    K (float): Strike price of the option.
    r (float): Risk-free interest rate most appropriate for this option.
    T (float): Number of days till the expiration date.
    H (float): Barrier Value.
    type (str): Type of the option. Either 'call' or 'put'. Defaults to 'call'.


## Create an instance of EOPricer Class
```python
pricer = EOPricer(S=None, K=None, r=None, T=None, H=None, option_type='call')
pricer.call_down_and_out(sigma=None)
```
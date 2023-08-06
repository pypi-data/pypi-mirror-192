import numpy as np
from scipy.stats import norm

class EOPricer:
    """A option modelled using Bjerksund e Stensland Formula do calculate de price of exotic options
    """

    def __init__(self, S=None, K=None, r=None, T=None, H=None, option_type='call'):
        """Initialize Option Class
        Args:
            S (float): Current price of the underlying asset.
            K (float): Strike price of the option.
            r (float): Risk-free interest rate most appropriate for this option.
            T (float): Number of days till the expiration date.
            H (float): Barrier Value.
            type (str): Type of the option. Either 'call' or 'put'. Defaults to 'call'.
        Returns:
            [type]: [description]
        """

        # Check variables and inputs
        if option_type.lower() not in ['call', 'put']:
            raise ValueError("Option can only be either a call or put.")

        
        
        
        _days_in_year = 252 

        # Assign values to the class
        self.S = S
        self.K = K
        self.r = r
        self.T = T / _days_in_year 
        self.H = H
        self.type = option_type.lower()

    def call_down_and_out(self, sigma):
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * sigma ** 2) * self.T) / (sigma * np.sqrt(self.T))
        d2 = d1 - sigma * np.sqrt(self.T)
        lambda_ = (self.r  + (sigma ** 2) / 2) / (sigma ** 2)
        X1 = np.log(self.S / self.H) / (sigma * np.sqrt(self.T)) + lambda_ * sigma * np.sqrt(self.T)
        X2 = np.log(self.H / self.S) / (sigma * np.sqrt(self.T)) + lambda_ * sigma * np.sqrt(self.T)
        Y1 = np.log(self.H**2 / (self.S * self.K)) / (sigma * np.sqrt(self.T)) + lambda_ * sigma * np.sqrt(self.T)
        Y2 = np.log(self.H / self.S) / (sigma * np.sqrt(self.T)) + lambda_ * sigma * np.sqrt(self.T)
        rho1 = np.sqrt((sigma**2 * self.T + (2 * self.r - 2 * 0 + sigma**2) * (X1 - self.T)) / (sigma**2 * self.T + (2 * self.r - 2 * 0 + sigma**2) * X1))
        rho2 = np.sqrt((sigma**2 * self.T + (2 * self.r - 2 * 0 + sigma**2) * (X2 - self.T)) / (sigma**2 * self.T + (2 * self.r - 2 * 0 + sigma**2) * X2))
        rho3 = np.sqrt((sigma**2 * self.T + (2 * self.r - 2 * 0 + sigma**2) * (Y1 - self.T)) / (sigma**2 * self.T + (2 * self.r - 2 * 0 + sigma**2) * Y1))
        rho4 = np.sqrt((sigma**2 * self.T + (2 * self.r - 2 * 0 + sigma**2) * (Y2 - self.T)) / (sigma**2 * self.T + (2 * self.r - 2 * 0 + sigma**2) * Y2))

        call_price = self.S * np.exp(0) * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
        call_price -= self.S * np.exp(0) * ((self.H / self.S) ** (2 * lambda_)) * norm.cdf(X1) 
        call_price += self.K * np.exp(-self.r * self.T) * ((self.H / self.S) ** (2 * lambda_ - 2)) * norm.cdf(X1 - sigma * np.sqrt(self.T)) 
        call_price += self.S * np.exp(0) * ((self.H / self.S) ** (2 * lambda_)) * ((rho1 * norm.cdf(rho1 * X1) + rho2 * norm.cdf(-rho2 * X1 - 2 * rho1 * np.sqrt(self.T)))) 
        call_price -= self.K * np.exp(-self.r * self.T) * ((self.H / self.S) ** (2 * lambda_ - 2)) * ((rho3 * norm.cdf(rho3 * Y1) + rho4 * norm.cdf(-rho4 * Y1 - 2 * rho3 * np.sqrt(self.T))))


        return call_price

    
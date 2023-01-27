import numpy as np
from chaos_game import *
import matplotlib.pyplot as plt

class Variations:
    
    def __init__(self, x, y, name):
        """
        defining the parameters in Variations and calling
        method transform()
        Parameters
        ----------
        x : x values.
        y : y values.
        name : str of staticmethod.
        Returns
        -------
        None.
        """
        self.x = x
        self.y = y
        self.name = name
        self.transform()
        
    @staticmethod
    def linear(x,y):
        """
        Static method with;
        Parameters
        ----------
        x : x values.
        y : y values.
        Returns
        -------
        x : x values.
        y : y values.
        """
        return (x,y)

    @staticmethod
    def handkerchief(x,y):
        """
        Static method with;
        Parameters
        ----------
        x : x values.
        y : y values.
        Returns
        -------
        x and y values but after completing calculation.
        """
        r = np.sqrt(x**2 + y**2)
        ø = np.arctan2(x,y) #theta
        return r*(np.sin(ø + r), np.cos(ø - r))
    
    @staticmethod
    def swirl(x,y):
        """
        Static method with;
        
        Parameters
        ----------
        x : x values.
        y : y values.
        Returns
        -------
        x and y values but after completing calculation.
        """
        r = np.sqrt(x**2 + y**2)
        return (x * np.sin(r**2) - y * np.cos(r**2), x * np.cos(r**2) + y * np.sin(r**2))
    
    @staticmethod
    def disc(x,y):
        """
        Static method with;
        
        Parameters
        ----------
        x : x values.
        y : y values.
        Returns
        -------
        x and y values but after completing calculation.
        """
        r = np.sqrt(x**2 + y**2)
        ø = np.arctan2(x,y) #theta
        return  ø/np.pi*(np.sin(np.pi * r)), ø/np.pi * (np.cos(np.pi * r))
    
    @staticmethod
    def heart(x,y):
        """
        Static method with;
        
        Parameters
        ----------
        x : x values.
        y : y values.
        Returns
        -------
        x and y values but after completing calculation.
        """
        r = np.sqrt(x**2 + y**2)
        ø = np.arctan2(x,y) #theta
        return r*(np.sin(ø*r), -np.cos(ø*r))
    
    @staticmethod
    def spherical(x,y):
        """
        Static method with;
        
        Parameters
        ----------
        x : x values.
        y : y values.
        Returns
        -------
        x and y values but after completing calculation.
        """
        r = np.sqrt(x**2 + y**2)
        return (1/r**2) * (x, y)
    
    def transform(self):
        """
        method in class that transforms the given x and y values and;
        Returns
        -------
        x1 : the x values of that staticmethod.
        y1 : the y values of that staticmethod.
        """
        name = self.name
        
        _func = getattr(Variations, name)
        #print('Function =:',_func(x,y))
        x1,y1 =_func(self.x,self.y)[0], _func(self.x,self.y)[1]
        return np.array([x1,y1])
    
    @classmethod
    def from_chaos_game(cls, ngon, name):
        """
        classmethod that creates an instance from ChaosGame
        and gets the X value to be used here
        Parameters
        ----------
        cls : class (Variations).
        name : str name of staticmethod.
        Returns
        -------
        an instance of Variations with different names.
        """
        
        #print(X[:,1],X[:,0])
        #print(X)
        return cls(ngon.X[:,0], -ngon.X[:,1], name)
    
def linear_combination_wrap(variation1, variation2):
    """
    Parameters
    ----------
    variation1 : first instance of class Variable that goes through
    classmethod from_chaos_game.
    variation2 : second instance of class Variable that goes through
    classmethod from_chaos_game.
    
    Returns
    -------
    Fucntion W.
    """
    v1 = variation1.transform()
    v2 = variation2.transform()
    
    #u,v = w * v1 + (1-w) * v2
    def W(coeffs):
        """
        
        Parameters
        ----------
        coeffs : weight values (w) that is defined in main code.
        Returns
        -------
        u : value to plot.
        v : value to plot.
        """
        w = coeffs
        u,v = w * v1 + (1-w) * v2
        return u,v
    return W

transformations = ["linear", "handkerchief", "swirl", "disc", 
                   "heart", "spherical"]

ngon = ChaosGame(4,1/3) #instance from ChaosGame
ngon.iterate(10000)
colors = ngon.gradient_color

if __name__ == '__main__':
    """Main code to run Part4b"""
    N = 100
    grid_values = np.linspace(-1, 1, N)
    x, y = np.meshgrid(grid_values, grid_values)
    x_values = x.flatten()
    y_values = y.flatten()
    
    variations = [Variations(x_values, y_values, version) for version in transformations]

    fig, axs = plt.subplots(2, 2, figsize=(9, 9))
    for i, (ax, variation) in enumerate(zip(axs.flatten(), variations)):
       
        u, v = variation.transform()
    
        ax.plot(u, -v, markersize=1, marker=".", linestyle="", c='black')
        ax.set_title(variation.name)
        ax.axis("off")
    
    fig.savefig("variations_4b.png")
    plt.show()

if __name__ == '__main__':
    """Main code to run Part4c"""
    fig, axs = plt.subplots(2, 2, figsize=(9, 9))
    for i, (ax, variation) in enumerate(zip(axs.flatten(), transformations)):
       
        val = Variations.from_chaos_game(ngon,variation)
        u, v = val.transform()
    
        ax.scatter(u, -v, marker=".", s=0.2, c=colors, cmap = 'viridis')
        ax.set_title(variation)
        ax.axis("off")
    
    fig.savefig("variations_4c.png")
    plt.show()

if __name__ == '__main__':
    """Main koden for å kjøre Part4d"""
    coeffs = np.linspace(0, 1, 4)
    
    variation1 = Variations.from_chaos_game(ngon, "linear")
    variation2 = Variations.from_chaos_game(ngon, "disc")
    
    variation12 = linear_combination_wrap(variation1, variation2)    
    
    fig, axs = plt.subplots(2, 2, figsize=(9, 9))
    for ax, w in zip(axs.flatten(), coeffs):
        u, v = variation12(w)
        
        ax.scatter(u, -v, s=0.2, marker=".", c=colors)
        ax.set_title(f"weight = {w:.2f}")
        ax.axis("off")
        
    fig.savefig("variations_4d.png")
    plt.show()
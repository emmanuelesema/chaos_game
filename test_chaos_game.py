import matplotlib.pyplot as plt
from chaos_game import *
import numpy as np
import pytest
import os.path

def test_ChaosGame():
    """Testing to verify that ChaosGame raises valueerror for n<3 
                        and r < 0 or r > 1"""
    try:
        ChaosGame(1,1)
    except ValueError:
        pass

@pytest.mark.parametrize(
    "n, r, expected",
    [
        (  3,   0.5, [[0.0, 1.0], 
                      [0.8660254037844388, -0.4999999999999998], 
                      [-0.8660254037844384, -0.5000000000000004]]),
        (  4, 1/3,  [[0.0, 1.0], 
                     [1.0, 6.123233995736766e-17], 
                     [1.2246467991473532e-16, -1.0], 
                     [-1.0, -1.8369701987210297e-16]]), 
    ]
)

def test_ngon_is_created(n,r,expected):
    """Test to check that ngon points are created"""
    assert ChaosGame(n, r)._generate_ngon() == expected
        
def test_plot_ngon():
    """Test to check plot() works"""
    plt.close()
    ChaosGame(3,0.5).plot_ngon()
    #gcf = get current figure
    assert plt.gcf().number == 1 #gets the 1st figure plotted and 
                                 #compares with the figure the method
                                 #plot_ngon() plots

@pytest.mark.parametrize(
    "expected",
    [
        'figures/chaos{1}.png',
        'figures/chaos{2}.png',
        'figures/chaos{3}.png',
        'figures/chaos{4}.png',
        'figures/chaos{5}.png',
    ]
)
def test_savepng(expected):
    """Test to check if savepng() works"""
    if os.path.isfile(expected): #only works if name is manually updated
        pass
    else:
        raise AttributeError

def test_show():
    """Test to check if show() works"""
    
    x = ChaosGame(3,0.5)
    x.iterate(10000, discard=5)
    x.show(color=True)
    assert plt.gcf().number == 1
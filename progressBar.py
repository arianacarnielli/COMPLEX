# -*- coding: utf-8 -*-
"""
Module for creating progress bars.

Typical usage example:
  import progressbar as p
  import time
  
  bar = p.Progressbar(150)
  for i in range(150):
    p.update(i+1)
    time.sleep(0.01)

See docstrings of the class for detailed explanations of the arguments.
"""

import sys

class ProgressBar:
  """
  Class for representing a progress bar.
  
  Attributes:
    maxValue: largest value being counted by the bar
    width: width used to represent the bar itself. The total width is width+7
      when counting the initial [, the final ], and the space for the
      percentage.
    symbol: symbol used in the progress bar, should be a single character.
  """
  
  def __init__(self, maxValue, width = 20, symbol="#"):
    self.maxValue = maxValue
    self.width = width
    self.symbol = symbol
    
  def update(self, val):
    """
    Updates the progress bar in the current line.
    
    Arguments:
      val: current value. Should be between 0 and self.maxVal (including both).
    """
    perc = val/self.maxValue
    qt = min(self.width, int(perc * self.width + 0.5))
    perc = min(100, int(perc * 100 + 0.5))
    sys.stdout.write("\r")
    sys.stdout.write("[{0:<{1}s}] {2:>3d}%".format(self.symbol*qt, self.width, perc))
    sys.stdout.flush()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 19:50:56 2023

@author: Mikhail Glagolev
"""

import unittest
import MDAnalysis as mda
import os
from mouse2.bond_autocorrelations import bond_autocorrelations
import numpy as np

test_dir = absolute_path = os.path.dirname(__file__)

test_file = os.path.join(test_dir, "helical_lamellae.data.gz")

tolerance = 1e-6

target = {
    "lamellae_flexible" : 
        { "k_max" : 10,
          "selection" : "type 1",
          "different_molecules" : False,
          "test_file" : "helical_lamellae.data.gz",
          "data" : np.asarray([
              1.0,
              0.204648203125,
              0.08333987862723215,
              0.04822373422475962,
              0.04239111735026042,
              0.028410007546164774,
              0.0326979833984375,
              0.0241927001953125,
              0.019064814758300783,
              0.017419686453683036,
              0.017799589029947917,
              ]),
         },
    "lamellae_helical" : 
        { "k_max" : 10,
          "selection" : "type 2",
          "different_molecules" : False,
          "test_file" : "helical_lamellae.data.gz",
          "data" : np.asarray([
              1.0,
              -0.016461666666666666,
              -0.2911587890625,
              0.8378388221153846,
              0.3077317708333333,
              -0.41193316761363635,
              0.607004609375,
              0.5848464409722223,
              -0.376908251953125,
              0.31830694754464284,
              0.747251171875
          ]),
         },
    "disordered_helices" :
        { "k_max" : 18,
          "selection" : None,
          "different_molecules" : False,
          "test_file" : "disordered_helices.pdb",
          "data" : np.asarray([
              1.0,
              -0.00041347082455952963,
              -0.3038591452205882,
              0.8871704711914062,
              0.4083623697916667,
              -0.4639172014508929,
              0.5886043419471154,
              0.7663565266927084,
              -0.3978091264204546,
              0.1958014892578125,
              0.9634552951388888,
              -0.13286221313476562,
              -0.16088459123883928,
              0.9480305989583333,
              0.23268154296875,
              -0.35744268798828127,
              0.7705703125,
              0.5165108642578125,
              -0.245722412109375
              ]),
         },
    "disordered_helices_different_mol" :
        { "k_max" : 25,
          "selection" : None,
          "different_molecules" : True,
          "test_file" : "disordered_helices.pdb",
          "data" : np.asarray([
              1.0,
              -0.0013696978246822635,
              -0.2720864159254191,
              0.7483043635768517,
              0.3199276627223801,
              -0.3440386446065531,
              0.4055456886398926,
              0.48207786202347586,
              -0.2358160696602932,
              0.10598854839717861,
              0.4571763657224635,
              -0.0643645341040315,
              -0.05886949897722338,
              0.3040254572739416,
              0.05214486917717573,
              -0.07994574252936434,
              0.12923324883774873,
              0.04798963242086223,
              -0.023802412829888986,
              0.007082524961524098,
              -5.407812847028001e-05,
              -0.012452094885233501,
              0.0014287276876650868,
              0.00400884942526295,
              -0.009362746053235562,
              -0.0040081568194204505
              ]),
         },
    }


class TestAutocorrelations(unittest.TestCase):
    
    def check_autocorrelations(self, target):
        test_file = target["test_file"]
        k_max = target["k_max"]
        selection = target["selection"]
        different_molecules = target["different_molecules"]
        target_data = target["data"]
        u = mda.Universe(test_file)
        result = bond_autocorrelations(u, k_max,
                                    different_molecules = different_molecules,
                                    selection = selection)
        ck = np.asarray(list(result["data"].values())[0])
        discrepancy = np.max(np.abs(ck - target_data))
        assert discrepancy <= tolerance
        
    def test_flexible_sk(self):
        self.check_autocorrelations(target["lamellae_flexible"])
        
    def test_helical_sk(self):
        self.check_autocorrelations(target["lamellae_helical"])
        
    def test_disordered_helices(self):
        self.check_autocorrelations(target["disordered_helices"])
        
    def test_disordered_helices_different_mol(self):
        self.check_autocorrelations(target["disordered_helices_different_mol"])
        
class TestLocalAlignment(unittest.TestCase):
    
    def check_local_alignment(self, target):
        test_file = target["test_file"]
        r_min = target["r_min"]
        r_max = target["r_max"]
        selection = target["selection"]
        same_molecule = target["same_molecule"]
        target_data = target["data"]
        mode = target["mode"]
        n_bins = target["n_bins"]
        id_pairs = target["id_pairs"]
        u = mda.Universe(test_file)
        result = local_alignment(u, r_min = r_min, r_max = r_max, ***)

        
if __name__ == "__main__":
    unittest.main()
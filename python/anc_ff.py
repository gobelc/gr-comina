#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy as np
from gnuradio import gr

class anc_ff(gr.sync_block):
    """
    This block clean-up a signal via minimizing LSE with a reference signal. Two outputs available: signal canceled (a tone for example) and the cleaned signal (error).
    """
    def __init__(self, forgetting_factor, size):
        gr.sync_block.__init__(self,
            name = "anc_ff",
            in_sig = [np.float32,np.float32],
            out_sig = [np.float32,np.float32])
        self.size = size
        self.forgetting_factor = forgetting_factor
        self.sigma_0 = 1
        self.h = (np.ones(self.size)).T
        self.theta = (np.zeros(size)).T
        self.sigma = self.sigma_0*np.identity(size)

    def work(self, input_items, output_items):
        out0 = output_items[0]
        out1 = output_items[1]
        
        signal = input_items[0][:]
        ref = input_items[1][:]

        salida  =    np.zeros(len(out0))
        error   =   np.ones(len(out1))
        forgetting_factor = self.forgetting_factor

        for n in range(0, len(out0)): 

            error[n] = signal[n] - np.matmul(self.h, self.theta)
            salida[n] = np.matmul(self.h, self.theta)

            self.h = np.roll(self.h,1)
            self.h[0] = ref[n]
            if ((forgetting_factor**n+np.matmul(np.matmul((self.h).T,self.sigma),self.h))<>0):
                self.K = (np.matmul(self.sigma,self.h)) / (forgetting_factor**n+np.matmul(np.matmul((self.h).T,self.sigma),self.h))
            self.sigma = np.matmul(np.identity(self.size)-np.matmul(self.K,(self.h).T),self.sigma)
            self.theta = self.theta + self.K*error[n]
            
            print "Coef:", self.theta
            print "K", self.K
            print "sihma", self.sigma 
            #salida[n] = signal[n] - error[n]
            

        out0[:] = salida
        out1[:] = error
        
        return len(output_items[0])
       
    

        


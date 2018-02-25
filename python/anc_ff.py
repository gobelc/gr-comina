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
    This block clean-up a signal via minimizing LSE with a reference signal. 
    Two outputs available: signal canceled (a tone for example) and the cleaned signal
    (error).
    """
    def __init__(self, forgetting_factor, size, refresh_number):
        gr.sync_block.__init__(self,
            name = "anc_ff",
            in_sig = [np.float32,np.float32],
            out_sig = [np.float32,np.float32])
        self.size = size
        self.forgetting_factor = forgetting_factor
        self.refresh_number = refresh_number
        self.sigma_0 = 1
        self.h = (np.ones(self.size)).T
        self.theta = (np.zeros(size)).T
        self.sigma = self.sigma_0*np.identity(size)
        self.K = (np.matmul(self.sigma,self.h)) / 
            (self.forgetting_factor+np.matmul(np.matmul(self.h.T,self.sigma),self.h))
        self.count = 0

    def work(self, input_items, output_items):
        out0 = output_items[0]
        out1 = output_items[1]
        signal = input_items[0][:]
        ref = input_items[1][:]
        salida  =    np.zeros(len(out0))
        error   =   np.ones(len(out1))
        forgetting_factor = self.forgetting_factor
        h = self.h
        theta = self.theta
        sigma = self.sigma
        K = self.K
        size = self.size
        count = self.count
        for n in range(0, len(out0)): 
            error[n] = signal[n] - np.matmul(h, theta)
            salida[n] = np.matmul(h, theta)
            h = np.roll(h,1)
            h[0] = ref[n]
            if count>self.refresh_number:
                count = 0
                forgetting_factor = self.forgetting_factor
            denominador = forgetting_factor**n+np.matmul(np.matmul(h.T,sigma),h)
            if denominador != 0:
                K = (np.matmul(sigma,h)) / denominador
            sigma = np.matmul(np.identity(size)-np.matmul(K,(h).T),sigma)
            theta = theta + K*error[n]
            self.h = h
            self.theta = theta
            self.sigma = sigma
            self.K = K
            count = count + 1
        out0[:] = salida
        out1[:] = error
        return len(output_items[0])
       
    

        


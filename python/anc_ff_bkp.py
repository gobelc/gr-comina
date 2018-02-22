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
    docstring for block anc_ff
    """
    def __init__(self, forgetting_factor, size):
        gr.sync_block.__init__(self,
            name="anc_ff",
            in_sig=[np.float32,np.float32],
            out_sig=[np.float32,np.float32])
        
        self.size = size
        self.forgetting_factor = forgetting_factor
        self.flag = True
        self.sigma_0 = 1
        self.h =(np.ones(self.size)).T
        self.theta = (np.zeros(size)).T
        self.sigma = self.sigma_0*np.ones((size,size))
        self.error=0
        self.salida=0
        self.counter=0


    def work(self, input_items, output_items):
        in0 = input_items[0]
        in1 = input_items[1]
        
        out0= output_items[0]
        out1= output_items[1]
        
        
        signal = input_items[0][:]
        ref = input_items[1][:]

        print signal
        print ref


        for n in range(0, len(output_items)):
            signal[n]


            self.error = signal[0] - np.matmul(self.h, self.theta)
            self.K = (np.matmul(self.sigma,self.h))/(self.forgetting_factor+np.matmul(np.matmul(self.h,self.sigma),(self.h).T))
            self.h = np.roll(self.h,1)
            self.h[0] = ref[0]
            self.sigma = np.matmul(np.identity(self.size)-np.matmul(self.K,(self.h).T),self.sigma)
            #self.forgetting_factor=self.forgetting_factor*self.forgetting_factor
            self.theta = self.theta + self.K*self.error
            salida = signal[0] - self.error
            self.counter = self.counter + 1

        print "error: ", self.error
        print "K: ", self.K
        print "sigma: ", self.sigma
        print "forgetting factor: ", self.forgetting_factor
        print "ref: ", self.h
        print "Filtro: ", self.theta
        print self.counter
        
    
        # Init parameters

        # <+signal processing here+>
        ''' THIS WORKS
        out0[:] = in0
        out1[:] = in1
        '''
 

        
        out0[:] = salida
        out1[:] = self.error

        
        return len(output_items[0])
       
    

        


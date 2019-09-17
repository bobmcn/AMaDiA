# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 14:55:31 2019

@author: Robin
"""

# if__name__ == "__main__":
#     pass

import sys
from PyQt5 import QtWidgets,QtCore,QtGui # Maybe Needs a change of the interpreter of Qt Creator to work there
import socket
import datetime
import platform
import errno
import os
import sympy

from sympy.parsing.latex import parse_latex
from sympy.parsing.sympy_parser import parse_expr

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
import scipy

import AMaDiA_Functions as AF
import AMaDiA_ReplacementTables as ART


##### SEE https://github.com/sympy/sympy_gamma/


class AMaS: # Astus' Mathematical Structure
    def __init__(self, string, Type = "Python"): # TODOMode: Not happy with the Mode thing...
        self.TimeStamp = AF.cTimeSStr()
        self.Type = Type # LaTeX = L , Python = P , Complex = C # TODOMode: Not happy with the Mode thing...
        self.string = string
        self.init()
        self.init_plot()
        self.init_history()
    
    def init(self):
        self.string = self.string.replace("integrate","Integral") # integrate takes 6 seconds to evaluate while Integral takes "no" time but both do the same
        self.string = self.string.replace("Integrate","Integral") # also doing this in case of capitalization stuff
        self.string = self.string.replace("integral","Integral")  # also doing this in case of capitalization stuff
        self.Text = self.string
        self.Evaluation = "Not evaluated yet."
        self.EvaluationEquation = "? = " + self.Text
        #self.Analyse() #TODO
        try:
            self.simpleConversion = AF.Convert_to_LaTeX(self.string) #TODO: Remove or change
        except ... :
            self.simpleConversion = "Fail"
        self.LaTeX = self.simpleConversion
        if self.Type == "C" or self.Type == "Complex": # TODOMode: Not happy with the Mode thing...
            self.LaTeX = self.simpleConversion # TODO
            
        elif self.Type == "L" or self.Type == "Latex": # TODOMode: Not happy with the Mode thing...
            self.LaTeX = self.simpleConversion
            
        elif self.Type == "P" or self.Type == "Python": # TODOMode: Not happy with the Mode thing...
            try:
                if self.string.count("=") >= 1 :
                    parts = self.string.split("=")
                    self.LaTeX = ""
                    for i in parts:
                        if len(i)>0:
                            self.LaTeX += sympy.latex( sympy.S(i,evaluate=False))
                        self.LaTeX += " = "
                    self.LaTeX = self.LaTeX[:-3]
                else:
                    self.LaTeX = sympy.latex( sympy.S(self.string,evaluate=False))
            except sympy.SympifyError :
                self.LaTeX = "Fail"
                
                
    def init_history(self):
        self.tab_1_is = False
        self.tab_1_ref = None
        self.tab_2_is = False
        self.tab_2_ref = None
        self.tab_3_is = False
        self.tab_3_ref = None
                
    def init_plot(self):
        if self.string.count("=")==0 and self.string.count("x")>=1:
            self.plotable = True
        else:
            self.plotable = False
        self.plot_data_exists = False
        self.plot_ratio = False
        self.plot_grid = True
        self.plot_xmin = -5
        self.plot_xmax = 5
        self.plot_steps = 1000
        self.plot_per_unit = False
        self.plot_x_vals = np.arange(10)
        self.plot_y_vals = np.zeros_like(self.plot_x_vals)
        
    
    def Analyse(self): #TODO: Make it work
        #TODO: keep parse_expr() in mind!!!
        # https://docs.sympy.org/latest/modules/parsing.html
        i_first = -1
        for i in ART.beginning_symbols:
            i_curr = self.string.find(ART.beginning_symbols[i])
            if i_curr != -1:
                if i_first == -1:
                    i_first = i_curr
                elif i_curr < i_first:
                    i_first = i_curr
    
    def Evaluate(self,EvalF = True): # TODOMode: Not happy with the EvalF thing...
        #TODO:CALCULATE MORE STUFF
        # https://docs.sympy.org/latest/modules/evalf.html
        # https://docs.sympy.org/latest/modules/solvers/solvers.html
        if self.string.count("=") == 1 :
            if self.Type == "P" or self.Type == "Python": # TODOMode: Not happy with the Mode thing...
                try:
                    temp = self.string
                    temp = "(" + temp
                    temp = temp.replace("=" , ") - (")
                    temp = temp + ")"
                    ans = parse_expr(temp)
                    ans = sympy.solve(ans)
                    self.Evaluation = "[ "
                    for i in ans:
                        if EvalF: # TODOMode: Not happy with the EvalF thing... BUT happy with i.evalf()!!!!!!
                            i = i.evalf()
                        i_temp = str(i)
                        i_temp = i_temp.rstrip('0').rstrip('.') if '.' in i_temp else i_temp
                        self.Evaluation += str(i)
                        self.Evaluation += " , "
                    self.Evaluation = self.Evaluation[:-3]
                    if len(self.Evaluation) > 0:
                        self.Evaluation += " ]"
                    else:
                        ans = parse_expr(temp)
                        ans = ans.evalf()
                        self.Evaluation = "True" if ans == 0 else "False: "+str(ans)
                        
                except sympy.SympifyError :
                    self.Evaluation = "Fail"
            if self.Type == "L" or self.Type == "Latex": # TODOMode: Not happy with the Mode thing...
                #TODO
                try:
                    ans = parse_latex(temp)
                    ans = sympy.solve(ans)
                    self.Evaluation = str(ans)
                    self.Evaluation = self.Evaluation.rstrip('0').rstrip('.') if '.' in self.Evaluation else self.Evaluation
                except sympy.SympifyError :
                    self.Evaluation = "Fail"
            self.EvaluationEquation = self.Evaluation + "   <==   "
            self.EvaluationEquation += self.Text
        else:
            if self.Type == "P" or self.Type == "Python": # TODOMode: Not happy with the Mode thing...
                try:
                    ans = parse_expr(self.string)
                    if EvalF: # TODOMode: Not happy with the EvalF thing...
                        ans = ans.evalf()
                    self.Evaluation = str(ans)
                    self.Evaluation = self.Evaluation.rstrip('0').rstrip('.') if '.' in self.Evaluation else self.Evaluation
                except sympy.SympifyError :
                    self.Evaluation = "Fail"
            if self.Type == "L" or self.Type == "Latex": # TODOMode: Not happy with the Mode thing...
                try:
                    ans = parse_latex(self.string)
                    if EvalF: # TODOMode: Not happy with the EvalF thing...
                        ans = ans.evalf()
                    self.Evaluation = str(ans)
                    self.Evaluation = self.Evaluation.rstrip('0').rstrip('.') if '.' in self.Evaluation else self.Evaluation
                except sympy.SympifyError :
                    self.Evaluation = "Fail"
            self.EvaluationEquation = self.Evaluation + " = "
            self.EvaluationEquation += self.Text
        return True #TODO: make it only return true if successful
                
    def EvaluateLaTeX(self):
        # https://docs.sympy.org/latest/modules/solvers/solvers.html
        try:
            ans = parse_latex(self.LaTeX)
            ans = ans.evalf()
            self.Evaluation = str(ans)
        except sympy.SympifyError :
            self.Evaluation = "Fail"
            
            
    def Plot_Calc_Values(self):
        if self.plotable:
            x = sympy.symbols('x')
            Function = parse_expr(self.string)
            
            if self.plot_per_unit:
                steps = 1/self.plot_steps
            else:
                steps = (self.plot_xmax - self.plot_xmin)/self.plot_steps
                
            self.plot_x_vals = np.arange(self.plot_xmin, self.plot_xmax+steps, steps)
            try:
                evalfunc = sympy.lambdify(x, Function , modules='sympy')
                self.plot_y_vals = evalfunc(self.plot_x_vals)
            except AttributeError as inst: # To Catch AttributeError 'ImmutableDenseNDimArray' object has no attribute 'could_extract_minus_sign'
                # This occures, for example, when trying to plot integrate(sqrt(sin(x))/(sqrt(sin(x))+sqrt(cos(x))))
                # This is a known Sympy bug since ~2011 and is yet to be fixed...  See https://github.com/sympy/sympy/issues/5721
                #print(inst.args)
                #if callable(inst.args):
                    #print(AttributeError.args())
                
                if self.Text.count("integrate")+self.Text.count("Integral") != 1:
                    evalfunc = sympy.lambdify(x, self.Text, modules='numpy')
                    self.plot_y_vals = evalfunc(self.plot_x_vals)
                    self.plot_y_vals = np.asarray(self.plot_y_vals)
                else:
                    temp_Text = self.Text
                    temp_Text = temp_Text.replace("integrate","")
                    temp_Text = temp_Text.replace("Integral","")
                    evalfunc = sympy.lambdify(x, temp_Text, modules='numpy')
                    
                    def F(x):
                        try:
                            return [scipy.integrate.quad(evalfunc, 0, y) for y in x]
                        except TypeError:
                            return scipy.integrate.quad(evalfunc, 0, x)
                    
                    self.plot_y_vals = evalfunc(self.plot_x_vals)
                    self.plot_y_vals = [F(x)[0] for x in self.plot_x_vals]
                    self.plot_y_vals = np.asarray(self.plot_y_vals)
                    
            self.plot_data_exists = True
            return True
        else:
            return False



# flowsim

Flowsim.py uses simple Carslaw and Jaeger (1959) solutions for one-dimensional (1D-) 
groundwater flow to simulate time-dependent variation in either hydraulic head or 
groundwater flux at specified locations in the aquifer. All the solutions in flowsim.py 
were derived for linear flow problems, which means that they can be superimposed (aggregated). 
It is possible to use these simple solutions to design conceptual, physical meaningful models, 
which simulate time series of hydraulic head or groundwater flux that are comparable to what 
can be observed in the field. Compared to conducting numerical modeling, flowsim.py has the 
advantage that it takes no time to design and set up a model, and it takes not time to run a 
simulation. It is therefore beneficial to use flowsim.py at an early stage of a hydrological 
modeling project, also when the project eventually needs to use more complex, numerical modeling 
to conduct the study and make the decisions.
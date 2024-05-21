## Author: Musiliu Bello
## Student-ID B1210259
## School of Computing, Engineering and Digital Technologies , Teesside University.

Monkeypox Disease Transmission Modelling

This NetLogo model simulates the transmission dynamics of monkeypox disease within a human and animal population. The model explores how factors such as initial outbreak size, human-to-human and animal-to-human transmission rates, recovery chance, and mortality rate influence the spread of the disease.

Model Structure

Agents:
Humans: Represented by green circles (susceptible), red circles (infected), and blue circles (recovered/immune).
Animals: Represented by white circles (susceptible) and yellow circles (carriers).
Globals:
Track infection rates, recovery counts, and mortality among humans and animals.
Store parameters like initial outbreak size, transmission rates, and recovery chance.
Behaviors:
Humans move around the environment and can become infected through contact with other infected humans or carrier animals.
Recovered humans gain immunity.
A small percentage of recovered humans may still be susceptible to infection.
Carrier animals can transmit the virus to susceptible humans.
The model runs until 100% of the human population is infected.

Model Execution

Open the model(ABM/MONKEYPOX_Transmission_Model.nlogo) in NetLogo 6.4.0.
Review the globals section to adjust parameters like initial outbreak size, transmission rates, and recovery chance.
Click the "Setup" button to initialize the model environment.
Click the "Go" button to start the simulation.
The model will run until all humans are infected.
You can stop the model intermitently to to inspect the transmission patterns at a certain points(14days, 21days,28days based on BCDC monkeypox data 2022 for incubation, recovery, and mortality periods)

Outputs

The model continuously updates various statistics during simulation, including:
Percentage of infected humans.
Number of recovered and deceased humans.
Human-to-human and animal-to-human transmission counts.
These statistics can be visualized through NetLogo's designed output monitor and plotting functionalities.

Purpose

This model serves as a simplified agent-based representation of monkeypox transmission. It can be used to:

Gain insights into the potential impact of different public health interventions regarding monkeypox, such as vaccination and isolation measures.
Explore the relative contributions of human-to-human and animal-to-human transmission to the overall outbreak.
Identify critical factors influencing disease spread and guide control strategies.

Disclaimer

This model is for research and educational purposes only and should not be used to make real-world predictions about monkeypox outbreaks. The complexity of real-world disease transmission often exceeds the capabilities of a single model.

Further Reading

Centers for Disease Control and Prevention: https://www.cdc.gov/poxvirus/mpox/index.html
World Health Organization: https://www.who.int/emergencies/situations/monkeypox-oubreak-2022

This readme manual provides a clear and concise overview of the model, its functionalities, and its purpose. It also includes disclaimers and references for further exploration.

For any difficulties or suggestions, please contact the author.

Thank you.
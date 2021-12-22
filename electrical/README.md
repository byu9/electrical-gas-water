# Electrical System Dataset

1. Specify parent/child relationship in [Topology](topology.py).

1. Specify the power line type between parent/children in
   [Power Lines](power_lines.py) as well as:

   * Distance
   * Ohms per mile by line_type
   * Apparent power limit volt amps by line_type
   * Current limit amps by line_type

1. Specify bus acessories in [Buses](buses.py):

   * Voltage high/low limits in volts
   * Renewable generation watts and vars at each point in time
   * Load watts and vars at each point in time
   * Charger and inverter efficiency

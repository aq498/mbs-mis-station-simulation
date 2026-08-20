import numpy as np
import matplotlib.pyplot as plt

# independent simulation variables
a = 0 # simulation start time 0-196
b = 48 # simulation stop time 0-196
dt = 0.1 # sampling interval (hour)

hours = np.arange(a, b, dt) 
n = len(hours)
day_time = hours % 24

# flow/peak
base_flow = 50
morning_peak = 350 * np.exp(-((day_time - 8) ** 2) / 2)
evening_peak = 300 * np.exp(-((day_time - 18) ** 2) / 2)

# flow/demand
passengers = np.maximum(0, base_flow + morning_peak + evening_peak + np.random.normal(0, 5, n))
bike_demand = np.maximum(0, passengers * 0.30 + np.random.normal(0, 2, n))

# sim loop
bikes = np.zeros(n)
dwell = np.zeros(n)
bikes[0] = 40  

for i in range(1, n):
    checkout = min(bike_demand[i], bikes[i-1])
    returns = checkout * 0.7
    
    # Dynamic resupply
    if bikes[i-1] < 15:
        redistribution = min(35, int(bike_demand[i] * 0.5) + 10)
    elif bikes[i-1] > 50:
        redistribution = -10
    else:
        redistribution = 0
        
    # sto cap
    bikes[i] = np.clip(bikes[i-1] - checkout + returns + redistribution, 0, 100)
    
    # dwell
    raw_dwell = 25 + 2 * (passengers[i] / 10)
    dwell[i] = np.clip(raw_dwell, 25, 45)

fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(hours, passengers, label="Passenger Flow (pax/15min)", color="blue", alpha=0.7)
ax.plot(hours, bike_demand, label="Bike Demand", color="green", alpha=0.8)
ax.plot(hours, bikes, label="Available Bikes", color="orange")
ax.plot(hours, dwell, label="Dwell Time (s)", color="red", linestyle="--")
ax.set_xlim(a, b)
ax.grid(True, alpha=0.3)
ax.set_xlabel("Hours")
ax.set_ylabel("Count / Time (s)")
ax.set_title("MBS-MIS Station Simulation Highlights")
ax.legend(loc="upper right")
fig.tight_layout()
fig.savefig("simulation_results.png", dpi=300, bbox_inches="tight")
plt.show()

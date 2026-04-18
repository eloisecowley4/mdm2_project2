import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_path = "../../Coding/MDM2_2/2/exp02H20141127_14h13.csv"
df = pd.read_csv(file_path)

time_range = slice(60000,80000)

# plt.plot(df["X1"][time_range], df["Y1"][time_range], color="red", label="fish 1")
# plt.plot(df["X2"][time_range], df["Y2"][time_range], color="blue", label="fish 2")

# plt.axis("equal")   # important for path data
# plt.legend()
# plt.savefig("Figures/plot.pdf")

plt.plot(np.arange(len(df["H1"][time_range])), df["H1"][time_range])
plt.show()
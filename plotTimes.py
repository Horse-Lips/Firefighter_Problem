import matplotlib.pyplot as plt
import sys

colours = ["tab:blue", "tab:orange", "tab:green", "tab:purple", "tab:gray"]
timeFiles = sys.argv[1::]

for i in range(len(timeFiles)):
    tFile = open(timeFiles[i], 'r')
    tList = tFile.readlines()

    pulpTimes = [float(i) for i in tList[0].strip().split(", ")]
    mznTimes  = [float(i) for i in tList[1].strip().split(", ")]

    plt.scatter(pulpTimes, mznTimes, c = colours[i], label = timeFiles[i])

plt.xlabel("PulP CBC Solver Times (Seconds)")
plt.ylabel("MiniZinc OR-Tools Solver Times (Seconds)")
plt.legend()
plt.show()

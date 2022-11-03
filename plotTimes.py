import plotly.express as px

timeFile = open("times.csv")
timeLists = timeFile.readlines()

pulpTimes = [float(i) for i in timeLists[0].strip().split(", ")]
mznTimes  = [float(i) for i in timeLists[1].strip().split(", ")]

print(pulpTimes)
print(mznTimes)

fig = px.scatter(x = pulpTimes, y = mznTimes)
fig.show()

with open('3blue1brown_stats.txt', 'r') as f:
    filedata = f.read()
data_stats = eval(filedata)

with open('3blue1brown_contents.txt', 'r') as f:
    filedata = f.read()
data_content = eval(filedata)

with open('3blue1brown_vids.txt', 'r') as f:
    filedata = f.read()
data_vids = eval(filedata)

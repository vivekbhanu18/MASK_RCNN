import pandas as pd
import pygal
from pygal.style import DarkStyle

'''
df=pd.read_csv("output.csv")
df=df.dropna()
print(df)

graph = pygal.Bar()    
graph.title="usage of plastic"
graph.x_labels=list(df['location'])
graph.add('plastic',list(df['plastic']))
graph.add('Non-plastic',list(df['non_plastic']))
graph.render_to_file('bar_chart.svg') 

'''
data=pd.read_csv('output.csv')
data=data.dropna()
new1_data=data.groupby(['date_created'],sort=False).sum()
date=list(set(list(data['date_created'])))
graph1 = pygal.Bar(style=DarkStyle)    
graph1.title="usage of plastic"
graph1.x_labels=date
graph1.add('plastic',list(new_data1['plastic']))
graph1.add('Non-plastic',list(new_data1['non_plastic']))
graph1.render_to_file('bar_chart.svg') 
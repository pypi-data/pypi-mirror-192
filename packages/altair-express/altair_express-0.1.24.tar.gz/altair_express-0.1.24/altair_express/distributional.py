
import altair as alt
import pandas as pd
import numpy as np

from .interactions import Interaction, apply_effect, process_effects

def create_hist_dataframe(data=None, *, x=None, y=None):
  # create data if x and y are pandas series
  if data is None:
    data = pd.DataFrame({})
    # case that x series is provided 
    if isinstance(x, pd.Series):
      data['x'] = x
      x = 'x'

    # case that y series is provided 
    if isinstance(y, pd.Series):
      data['y'] = y
      y = 'y'
  elif isinstance(data, pd.Series):
    data = pd.DataFrame({'x':data})
    x = 'x'
  
  return data,x,y

def hist(data=None,x=None,color=None, max_bins=10,width=200,height=50,effects=None,x_axis = alt.Axis(),y_axis=alt.Axis()):
  # ensures that data is the data and x and y are column names
  data,x,y = create_hist_dataframe(data=data,x=x) 

  fill="steelblue"

  if color and color not in data.columns:
    fill = color
    color = None

  chart = alt.Chart(data)

  if x is not None:
    chart = chart.mark_bar(color=fill).encode(
            alt.X(f'{x}:Q', bin=alt.Bin(maxbins=max_bins), axis=x_axis),alt.Y('count()',axis=y_axis)
              ) 

    if color:
      chart = chart.encode(
        alt.Color(f'{color}:N'), opacity=(alt.value(0.5))
      )
  else:
    raise ValueError('[hist] no x value provided')

    
  if effects:
    chart = process_effects(chart,effects)

  return chart.properties(
          width=width,
          height=height
      )


def violin_plot(data=None,y=None,groupby=None, yAxis=None,xAxis=alt.Axis(labels=False, values=[0],grid=False, ticks=True),interactive=False,filters=None):
  if filters is None:
    filters = []

  facet_vars = [None]
  if groupby:
    facet_vars=pd.unique(data[groupby])


  charts =[]

  for index,variable in enumerate(facet_vars):
    # filter to unique value
    chart = alt.Chart(data=data)

    # filter to only one variable
    if variable is not None:
      chart=chart.transform_filter(
          alt.FieldEqualPredicate(field=groupby, equal=variable)
      )

    if yAxis is None:
      if index == 0:
        yAxis = alt.Axis(grid=False, ticks=True)
    else:
      if index != 0:
        yAxis = None
          
    chart = chart.mark_area().transform_density(
        y,
        as_=[y, 'density'],
    ).transform_stack(
        stack= "density",
        groupby= [y],
      as_= ["x", "x2"],
      offset= "center"
    ).encode(
        y=alt.Y(f'{y}:Q',axis=yAxis),
        x=alt.X(
            field='x',
            impute=None,
            title=None,
            type ="quantitative",
            axis=xAxis,
        ),
            x2=alt.X2(field = "x2")

    )


  
    if filters:
      for filter in filters:
        chart = chart.transform_filter(filter)
    
    charts.append(chart.properties(width=100,title = alt.TitleParams(text = variable )))
  final_chart = alt.hconcat(charts=charts,spacing=0)
  
  return final_chart


def countplot(data=None,x=None,xAxis=alt.Axis(),yAxis=alt.Axis(),sort='descending', limit=15, effects=None,width=250,height=150):
  

  if data is None:
    if x is None:
      raise ValueError('[countplot] no data or data series provided.')
    data = pd.DataFrame({})
    if isinstance(x, pd.Series):
      data['x'] = x
      x = 'x'

  # if x 

  sort_order =  '-y' if sort=='descending' else 'y'
  chart = alt.Chart(data).mark_bar().encode(
      alt.X(field=f'{x}',axis=xAxis,sort=sort_order), # remove the sort as that will keep it consistent with the background
      alt.Y(f'count({x}):Q',axis=yAxis)
  )
   
  if effects:
    chart = process_effects(chart,effects)

   
  return chart.properties(
          width=width,
          height=height
      )


def heatmap(data=None):
  if data is None:
    raise ValueError('[heatmap] no data or data series provided.')
  
  
  source = pd.DataFrame(data.unstack().reset_index().rename(columns={0:"value"}))


  x_variable = source.columns[0]
  y_variable = source.columns[1]

  
  chart = alt.Chart(source).mark_rect().encode(
    x=f'{x_variable}:O',
    y=f'{y_variable}:O',
    color='value:Q'
  )
  return chart
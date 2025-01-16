import pandas as pd 
import plotly.express as px 
import plotly.graph_objects as go


def barplot(df: pd.DataFrame, x: str, y: str, title: str, text: str) -> go.Figure:
    '''
    Creates a plotly bar graph and returns a go.figure() object
    '''
    fig1 = px.bar(df, x=x, y=y, text=text, text_auto='.3s', title=title)

    # Update the trace (bar) properties
    fig1.update_traces(
        textfont_size=12, textposition='outside', cliponaxis=True)

    # Update the layout properties
    fig1.update_layout(
        uniformtext_minsize=11,
        uniformtext_mode='show',
        xaxis_tickangle=90,
        xaxis=dict(tickfont=dict(size=12)),
        yaxis=dict(tickfont=dict(size=12)),
        font=dict(family="Times New Roman"),
        xaxis_title="Genre",
        yaxis_title="Count",
        title=dict(
            font=dict(size=24),
            y=0.9,
            x=0.5,
            xanchor='center',
            yanchor='top'
        ),
        width=1000,
        height=500,
        margin=dict(t=100, b=40, l=40, r=40)
    )
    # Update the x-axis font family
    fig1.update_xaxes(title_font=dict(family="Times New Roman"))
    return fig1


def scatterplot(df: pd.DataFrame,
                x: str, y: str, color: str,
                title: str,
                xaxis_title: str = "xaxis_title",
                yaxis_title: str = "yaxis_title") -> go.Figure:
   '''
    Creates a plotly scatter plot and returns a go.Figure() object
   '''
   fig2 = px.scatter(df, x=x, y=y, color=color, title=title)
   fig2.update_layout(
       xaxis_title=xaxis_title,
       yaxis_title=yaxis_title,
       width=1000, height=500,
       title=dict(
           font=dict(size=24),
           y=0.9,
           x=0.5,
           xanchor='center',
           yanchor='top'
       ),
       xaxis=dict(tickfont=dict(size=12)),
       yaxis=dict(tickfont=dict(size=12)),
       title_x=0.5)
   fig2.update_traces(marker=dict(size=11, opacity=0.5))
   return fig2

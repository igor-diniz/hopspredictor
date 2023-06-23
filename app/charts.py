import streamlit as st
import json
import plotly.graph_objects as go


def draw_bar_chart(predictions):
    predictions = json.loads(predictions)

    # Extract the prediction values
    categories = ["Overall", "Herbal", "Citrus"]
    min_values = list(map(lambda x: round(x, 3), predictions["min_predictions"][0]))
    max_values = list(map(lambda x: round(x, 3), predictions["max_predictions"][0]))
    avg_values = list(map(lambda x: round(x, 3), predictions["average_predictions"][0]))

    # Create the bar chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=categories,
        y=min_values,
        name='Min',
        text=min_values,
        textposition='auto',
        marker_color='#e9d8a6'
    ))

    fig.add_trace(go.Bar(
        x=categories,
        y=avg_values,
        name='Avg',
        text=avg_values,
        textposition='inside',
        marker_color='#94d2bd'
    ))

    fig.add_trace(go.Bar(
        x=categories,
        y=max_values,
        name='Max',
        text=max_values,
        textposition='auto',
        marker_color='#0a9396'
    ))

    fig.update_layout(
        barmode='group',
        title={
            'text': 'Prediction Ranges for Aromas',
            'font': {'size': 24}
        },
        xaxis={
            'title': 'Aromas',
            'title_font': {'size': 14},
            'tickfont': {'size': 16}
        },
        yaxis={
            'title': 'Strength ( 1 - 5 )',
            'title_font': {'size': 16},
        },
        width=800,  # Set the chart width
        height=500,  # Set the chart height
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)


def draw_polygonal_chart(predictions):
    predictions = json.loads(predictions)

    categories = ["Overall", "Herbal", "Citrus"]
    avg_values = list(map(lambda x: round(x, 3), predictions["average_predictions"][0]))

    # Create the radar chart
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=avg_values + [avg_values[0]],  # Close the shape by repeating the first value
        theta=categories + [categories[0]],  # Close the shape by repeating the first category
        fill='toself',
        line_color='skyblue',
        hovertemplate='Category: %{theta}<br>Value: %{r:.2f}',
        text=[f"{val:.2f}" for val in avg_values],  # Add text values
        mode='markers+text+lines',
        textposition="middle center",  # Set text position
        textfont=dict(color='black', size=13),  # Set text color and size
    ))

    # Customize layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(range=[0, 5], visible=True, tickcolor='black', tickfont=dict(color='black', size=14)),
            angularaxis=dict(showticklabels=True, tickangle=0, tickfont=dict(size=16)),
        ),
        showlegend=False,
        title={
            "text": "Aromas Distribution",
            "font": {"size": 24}
        },
        height=600,  # Increase the height of the chart
        width=600,  # Increase the width of the chart
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

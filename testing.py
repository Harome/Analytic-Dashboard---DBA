import dash
from dash import html
import matplotlib.pyplot as plt
import io
import base64

from Data.Clean_data.defineddata import (
    create_gender_plot,
    plot_total_number_of_schools_by_sector,
    plot_total_number_of_schools_by_region
)

# Convert matplotlib figure to base64 image
def fig_to_base64_img(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return f"data:image/png;base64,{encoded}"

# Generate images
gender_img = fig_to_base64_img(create_gender_plot())
sector_img = fig_to_base64_img(plot_total_number_of_schools_by_sector())
region_img = fig_to_base64_img(plot_total_number_of_schools_by_region())

# Dash setup
app = dash.Dash(__name__)
app.title = "Test Graph Display"

app.layout = html.Div([
    html.H1("📊 Graph Render Test", style={'textAlign': 'center'}),

    html.H3("Gender-Based Enrollment"),
    html.Img(src=gender_img, style={'maxWidth': '80%', 'display': 'block', 'margin': 'auto'}),

    html.H3("Number of Schools by Sector"),
    html.Img(src=sector_img, style={'maxWidth': '80%', 'display': 'block', 'margin': 'auto'}),

    html.H3("Number of Schools by Region"),
    html.Img(src=region_img, style={'maxWidth': '80%', 'display': 'block', 'margin': 'auto'}),
])

if __name__ == '__main__':
    app.run(debug=True)

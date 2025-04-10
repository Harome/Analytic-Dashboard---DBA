from dash import Dash, html
from components.layout import create_layout
from components.callbacks import register_callbacks

app = Dash(__name__)

app.layout = create_layout(app)

register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)
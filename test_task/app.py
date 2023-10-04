from dash import html, Output, Input, dcc
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import (DashProxy,
                                    ServersideOutputTransform,
                                    MultiplexerTransform)
import dash_mantine_components as dmc
import sqlite3
import pandas as pd
import plotly.express as px

CARD_STYLE = dict(withBorder=True,
                  shadow="sm",
                  radius="md",
                  style={'height': '400px'})

class EncostDash(DashProxy):
    def __init__(self, **kwargs):
        self.app_container = None
        super().__init__(transforms=[ServersideOutputTransform(),
                                     MultiplexerTransform()], **kwargs)

app = EncostDash(name=__name__)

conn = sqlite3.connect('testDB.db')
cursor = conn.cursor()

query = "SELECT * FROM sources"
df = pd.read_sql_query(query, conn)

def get_layout():
    return html.Div([
        dmc.Paper([
            dmc.Grid([
                dmc.Col([
                    dmc.Card([
                        html.Div(id="general-info"),
                        dcc.Dropdown(
                            id="state-filter",
                            options=[{"label": state, "value": state} for state in df["state"].unique()],
                            multi=True,
                            placeholder="Фильтр по состояниям"),
                        ],
                        **CARD_STYLE)
                ], span=6),
                dmc.Col([
                    dmc.Card([
                        dcc.Graph(id="pie-chart")],
                        **CARD_STYLE)
                ], span=6),
                dmc.Col([
                    dmc.Card([
                        dcc.Graph(id="gantt-chart")],
                        **CARD_STYLE)
                ], span=12),
            ], gutter="xl",)
        ])
    ])

app.layout = get_layout()
@app.callback(
    Output("general-info", "children"),
    Input("state-filter", "value")
)
def update_general_info(selected_states):
    if selected_states:
        filtered_df = df[df["state"].isin(selected_states)]
        if not filtered_df.empty:
            info = filtered_df.iloc[0]
        else:
            raise PreventUpdate("Нет данных для выбранных состояний.")
    else:
        info = df.iloc[0]

    required_columns = ['client_name', 'shift_day', 'endpoint_name', 'state_begin', 'state_end']
    if not all(column in info.index for column in required_columns):
        raise PreventUpdate("В DataFrame отсутствуют необходимые столбцы.")
    client_info = html.Div([
        html.P(f"Клиент: {info['client_name']}", style={'font-weight': 'bold', 'font-size': '20px'}),
        html.P(f"Сменный день: {info['shift_day']}"),
        html.P(f"Точка учета: {info['endpoint_name']}"),
        html.P(f"Начало периода: {info['state_begin']}"),
        html.P(f"Конец периода: {info['state_end']}")
    ], style={'margin-bottom': '20px'})
    return client_info



@app.callback(
    Output("pie-chart", "figure"),
    Input("state-filter", "value")
)
def update_pie_chart(selected_states):
    fig = px.pie(df, names="state")
    fig.update_layout(
        margin=dict(t=10),  
    )
    return fig


@app.callback(
    Output("gantt-chart", "figure"),
    Input("state-filter", "value")
)
def update_gantt_chart(selected_states):
    if selected_states:
        filtered_df = df[df["state"].isin(selected_states)]
    else:
        filtered_df = df
    fig = px.timeline(filtered_df, x_start="state_begin", x_end="state_end", y="state", title="Диаграмма состояния")
    fig.update_layout(
        showlegend=False,
        title=dict(text="Диаграмма состояния", x=0.5)
    )
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table

app = dash.Dash()

df = pd.read_csv('movies_initial.csv')
df = df[df["imdbVotes"] >= 1000]

genres = df['genre'].value_counts().index.tolist()

app.layout = html.Div([
    dcc.Dropdown(
        id='genre-dropdown',
        options=[{'label': genre, 'value': genre} for genre in genres],
        value=genres[0]
    ),
    html.Div(id='output-container')
])

@app.callback(
    dash.dependencies.Output('output-container', 'children'),
    [dash.dependencies.Input('genre-dropdown', 'value')])
def display_top_movies(selected_genre):
    dff = df[df['genre'] == selected_genre].nlargest(20, 'imdbRating')
    return html.Table([
        html.Thead([
            html.Tr([
                html.Th('Title', style={'border': '1px solid black', 'padding': '5px', 'background-color': 'lightgray'}),
                html.Th('Year', style={'border': '1px solid black', 'padding': '5px', 'background-color': 'lightgray'}),
                html.Th('imdbRating', style={'border': '1px solid black', 'padding': '5px', 'background-color': 'lightgray'}),
                html.Th('imdbVotes', style={'border': '1px solid black', 'padding': '5px', 'background-color': 'lightgray'}),
                html.Th('Metacritic', style={'border': '1px solid black', 'padding': '5px', 'background-color': 'lightgray'}),
                html.Th('Country', style={'border': '1px solid black', 'padding': '5px', 'background-color': 'lightgray'})
            ])
        ]),
        html.Tbody([            html.Tr([                html.Td(dff.iloc[i]['title'], style={'border': '1px solid black', 'padding': '5px'}),
                html.Td(dff.iloc[i]['year'], style={'border': '1px solid black', 'padding': '5px'}),
                html.Td(dff.iloc[i]['imdbRating'], style={'border': '1px solid black', 'padding': '5px'}),
                html.Td(dff.iloc[i]['imdbVotes'], style={'border': '1px solid black', 'padding': '5px'}),
                html.Td(dff.iloc[i]['metacritic'], style={'border': '1px solid black', 'padding': '5px'}),
                html.Td(dff.iloc[i]['country'], style={'border': '1px solid black', 'padding': '5px'})
            ]) for i in range(len(dff))
        ])
    ], style={'border-collapse': 'collapse'})

if __name__ == '__main__':
    app.run_server(debug=True)
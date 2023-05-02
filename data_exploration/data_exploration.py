import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table
import plotly.express as px

app = dash.Dash(__name__)
server = app.server

df = pd.read_csv('data_exploration/movies_initial.csv')
df = df[df["imdbVotes"] >= 1000]

genres = df['genre'].value_counts().index.tolist()

app.layout = html.Div([    html.H1(children='Top 20 Movies by Genre', style={'textAlign': 'center'}),    dcc.Dropdown(id='genre-dropdown', options=[{'label': genre, 'value': genre} for genre in genres], value=genres[0], style={'width': '50%', 'margin': '0 auto'}),
    html.Br(),
    html.Div([        html.Div(id='output-container', style={'width': '100%', 'display': 'inline-block', "padding-top": "10px"})    ], style={'display': 'flex', "padding":"10px",'flex-wrap': 'wrap', 'align-items': 'center', 'justify-content': 'center', 'margin': '0 auto'})
])

def clean_year_string(year_string):
    return ''.join(c for c in year_string if c.isdigit())

@app.callback(
    dash.dependencies.Output('output-container', 'children'),
    [dash.dependencies.Input('genre-dropdown', 'value')])
def display_top_movies(selected_genre):
    dff = df[df['genre'] == selected_genre].nlargest(20, 'imdbRating')
    dff['year'] = dff['year'].apply(clean_year_string).astype(int)
    min_year = dff['year'].min()
    max_year = dff['year'].max()
    yearly_counts = dff['year'].value_counts().reindex(range(min_year, max_year+1), fill_value=0).reset_index()
    yearly_counts.columns = ['year', 'count']
    fig = px.bar(yearly_counts.sort_values('count', ascending=True), x='count', y='year',orientation='h',title=f'Number of Movies in Top 20 per Year and Category for {selected_genre}')
    max_count = yearly_counts['count'].max()
    fig.update_layout(
        xaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=1,
            tickvals=list(range(0, max_count + 1, 2))
        ),
        plot_bgcolor='#f7f7f7',
        paper_bgcolor='#f7f7f7',
        font=dict(color='#444')
    )
    return html.Div([
    html.Div([
        html.Table([
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
            html.Tbody([
                html.Tr([
                    html.Td(dff.iloc[i]['title'], style={'border': '1px solid black', 'padding': '5px'}),
                    html.Td(dff.iloc[i]['year'], style={'border': '1px solid black', 'padding': '5px'}),
                    html.Td(dff.iloc[i]['imdbRating'], style={'border': '1px solid black', 'padding': '5px'}),
                    html.Td(dff.iloc[i]['imdbVotes'], style={'border': '1px solid black', 'padding': '5px'}),
                    html.Td(dff.iloc[i]['metacritic'], style={'border': '1px solid black', 'padding': '5px'}),
                    html.Td(dff.iloc[i]['country'], style={'border': '1px solid black', 'padding': '5px'})
                ]) for i in range(len(dff))
            ])
        ], style={'border-collapse': 'collapse', "padding":"10px"})
    ], style={'flex': '1'}),
    dcc.Graph(figure=fig, style={'flex': '1'})
], style={'display': 'flex', 'flex-wrap': 'wrap'})
if __name__ == '__main__':
    app.run_server(debug=True)
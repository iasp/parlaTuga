import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State, no_update
from dash.dependencies import ALL
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable

# Data sources
df_donut = pd.read_csv('Downloads/donutdata.csv')
df_funnel = pd.read_csv('Downloads/funneldata.csv')
df_vote = pd.read_csv('Downloads/votedata2.csv')
df_vote['Unanimous_Or_Not'] = df_vote['Unanimous_Or_Not'].replace({'N': 'Not Unanimous', 'Y': 'Unanimous'})
df_vote['Approved_Or_Rejected'] = df_vote['Approved_Or_Rejected'].replace({'Aprovado': 'Approved', 'Rejeitado': 'Rejected'})
df_detalhe = pd.read_csv('Downloads/detalhevoto.csv')

# Color scheme
blue_shades = [
    '#125699', '#0d3963', '#06294a', '#032c52', '#064a8a'
]

color_map = {
    'Proposta de Lei': '#0C7BDC',
    'Projeto de Lei': '#0c55dc',
    'Inquérito Parlamentar': '#FFC20A',
    'Projeto de Resolução': '#40B0A6',
    'Projeto de Deliberação': '#5D3A9B'
}

# Sidebar options in the desired order, with optional descriptions and separators
sidebar_options = [
    {"label": "PRES. AR", "value": "R", "description": "José P. Ag-Bra"},
    {"label": "GOVERNO", "value": "V", "description": "Aliança Dem."},
    {"label": "────────────", "value": "sep1", "disabled": True},
    {"label": "AÇORES", "value": "A", "description": "AL Açores"},
    {"label": "MADEIRA", "value": "M", "description": "AL Madeira"},
    {"label": "────────────", "value": "sep2", "disabled": True},
    {"label": "BE", "value": "BE", "description": "Bloco de Esq."},
    {"label": "CDS-PP", "value": "CDS-PP", "description": "CDS-PP"},
    {"label": "CH", "value": "CH", "description": "Chega"},
    {"label": "IL", "value": "IL", "description": "Ini. Liberal"},
    {"label": "L", "value": "L", "description": "Livre"},
    {"label": "PAN", "value": "PAN", "description": "PAN"},
    {"label": "PCP", "value": "PCP", "description": " PCP"},
    {"label": "PS", "value": "PS", "description": "PS"},
    {"label": "PSD", "value": "PSD", "description": "PSD"},
    {"label": "────────────", "value": "sep3", "disabled": True}
]

# Only pass real options and separators to dcc.RadioItems
radio_options = [
    {"label": opt["label"], "value": opt["value"], "disabled": opt.get("disabled", False)}
    for opt in sidebar_options
]

# Styles
SIDEBAR_STYLE = {
    "position": "fixed", "top": 0, "left": 0, "bottom": 0, "width": "30%",
    "padding": "1px 1px", "background-color": "black", "color": "white",
    "paddingTop": "50px",
    "overflowY": "auto", "fontFamily": "Dash Digital-7, monospace", "fontSize": "9px", "zIndex": 1
}

VISUALS_STYLE = {
    "position": "fixed", "top": 0, "left": "10%", "bottom": 0, "width": "25%",
    "padding": "0", "background-color": "#111", "color": "white", "paddingTop": "45px",
    "overflowY": "hidden", "fontFamily": "Dash Digital-7, monospace", "zIndex": 1,
    "display": "flex", "flexDirection": "column", "gap": "0", "height": "100vh"
}

CONTENT_STYLE = {
    "margin-left": "35%",
    "padding": "2rem 0 2rem 1rem",
    "backgroundColor": "black",
    "minHeight": "100vh",
    "color": "white",
    "fontFamily": "Dash Digital-7, monospace",
    "overflowX": "hidden",
    "width": "100vw"
}

style_table = {
    'textAlign': 'left',
    'minWidth': '50px', 
    'maxHeight': '300px',
    'whiteSpace': 'normal',
    'backgroundColor': 'black',
    'color': 'white',
    'border': '0.1px solid grey',
    'overflowY': 'auto',
    'overflowX': 'auto',
    'fontSize': '6px',
    'fontFamily': 'Dash Digital-7, monospace',
    'padding': '2px 4px',
    'width': '60vw',
    'lineHeight': '0.2',
}

style_cell = {
    'textAlign': 'center', 'minWidth': '55px', 'whiteSpace': 'normal',
    'backgroundColor': 'black', 'color': 'white', 'border': '0.1px solid grey',
    'fontSize': '6.5px', 'fontFamily': 'Dash Digital-7, monospace'
}

style_header = {
   'backgroundColor': '#222',
    'fontWeight': 'bold',
    'fontSize': '8px',
    'fontFamily': 'Dash Digital-7, monospace',
    'padding': '1px 2px',
    'lineHeight': '1.0',
}

style_cell_conditional=[
    {
        'if': {'column_id': 'Vote_ID'},
        'minWidth': '20px',
        'width': '20px',
        'maxWidth': '20px',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'padding': '2px 4px',
    },
]

# Dash Digital-7 font import via CDN
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://fonts.cdnfonts.com/css/dash-digital-7"
]

app = Dash(__name__, external_stylesheets=external_stylesheets)

horizontal_bar_style = {
    "width": "100%",
    "backgroundColor": "#f5970a",
    "color": "black",
    "fontFamily": "Dash Digital-7, monospace",
    "fontSize": "20px",
    "padding": "5px 10px",
    "position": "fixed",
    "top": 0,
    "left": 0,
    "zIndex": 1000,
    "textAlign": "center",
    "borderBottom": "1px solid #444"
}

horizontal_bar = html.Div(
    html.H2("p a r l a t 👀👀 g a _________________________________________________  ibopax.substack.com", className="display-6", style={
        "fontFamily": "Dash Digital-7, monospace",
        "fontSize": "15px",
        "margin": 0
    }),
    style=horizontal_bar_style
)

# Sidebar with single dcc.RadioItems and description
sidebar = html.Div([
    html.H2("👇", className="display-6", style={"fontFamily": "Dash Digital-7, monospace", "fontSize": "30px"}),
    html.Hr(),
    dcc.RadioItems(
        id='author_selector_radio',
        options=radio_options,
        value=None,
        labelStyle={'display': 'block', 'margin-bottom': '2px', 'fontFamily': 'Dash Digital-7, monospace'},
        style={'color': 'white', 'fontFamily': 'Dash Digital-7, monospace', 'fontSize': '10px'},
        inputStyle={"marginRight": "6px"},
    ),
    html.Div(id='sidebar-description', style={"color": "#888", "marginTop": "10px", "fontSize": "10px"})
], style=SIDEBAR_STYLE)

# Two visuals
visuals = html.Div([
    html.Div(id='donut_chart_container', style={"height": "50%", "margin": "0", "padding": "0"}),
    html.Div(id='funnel_chart_container', style={"height": "50%", "margin": "0", "padding": "0"}),
], style=VISUALS_STYLE)

# And the table
content = html.Div([
    dbc.Row([
        dbc.Col(html.H4("", style={"color": "white", "marginBottom": "5px", "fontFamily": "Dash Digital-7, monospace"}), width="auto"),
    ], align="right", className="mb-2", style={"gap": "10px"}),

    dbc.Row([
        # Approved summary and filter
        dbc.Col([
            html.Div(id="approved-summary", style={"color": "white", "fontSize": "12px", "marginBottom": "2px", "fontFamily": "Dash Digital-7, monospace"}),
            dcc.RadioItems(
                id='approved-filter',
                options=[
                    {'label': 'Aprovado', 'value': 'Approved'},
                    {'label': 'Rejeitado', 'value': 'Rejected'}
                ],
                value=None,
                inline=True,
                labelStyle={'margin-right': '10px', 'fontSize': '9px', 'color': '#d9d9d9', 'fontFamily': 'Dash Digital-7, monospace'}
            ),
        ], width=2),

        # Unanimous summary and filter
        dbc.Col([
            html.Div(id="unanimous-summary", style={"color": "white", "fontSize": "12px", "marginBottom": "2px", "fontFamily": "Dash Digital-7, monospace"}),
            dcc.RadioItems(
                id='unanimous-filter',
                options=[
                    {'label': 'Unânime', 'value': 'Unanimous'},
                    {'label': 'Contestado', 'value': 'Not Unanimous'}
                ],
                value=None,
                inline=True,
                labelStyle={'margin-right': '10px', 'fontSize': '9px', 'color': '#d9d9d9', 'fontFamily': 'Dash Digital-7, monospace'}
            ),
        ], width=2),

        # Blocksplit summary and filter
        dbc.Col([
            html.Div(id="blocksplit-summary", style={"color": "white", "fontSize": "12px", "marginBottom": "2px", "fontFamily": "Dash Digital-7, monospace"}),
            dcc.RadioItems(
                id='blocksplit-filter',
                options=[
                    {'label': 'Coeso', 'value': 'Block Vote'},
                    {'label': 'Fragmentado', 'value': 'Split Vote'}
                ],
                value=None,
                inline=True,
                labelStyle={'margin-left': '10px', 'fontSize': '9px', 'color': '#d9d9d9', 'fontFamily': 'Dash Digital-7, monospace'}
            ),
        ], width=2),
    ], className="mb-2", style={"justifyContent": "flex-start"}),

    # Main table and detail view of vote id
    DataTable(
        id='vote-table',
        columns=[
            {"name": "ID_Voto", "id": "Vote_ID"},
            {"name": "Contra", "id": "Contra"},
            {"name": "A Favor", "id": "Favor"},
            {"name": "Abstenção", "id": "Abstenção"},
        ],
        data=[],
        filter_action="native",
        sort_action="native",
        style_table=style_table,
        style_cell=style_cell,
        style_header=style_header,
        fixed_rows={'headers': True},
        page_action='none',
    ),
    html.Div(id='detalhe-view', style={"marginTop": "30px", "fontFamily": "Dash Digital-7, monospace"})
], style=CONTENT_STYLE)

app.layout = html.Div(
    [horizontal_bar, sidebar, visuals, content],
    style={"overflowX": "hidden", "overflowY": "hidden", "fontFamily": "Dash Digital-7, monospace"}
)

# Callback for sidebar description
@app.callback(
    Output('sidebar-description', 'children'),
    Input('author_selector_radio', 'value')
)
def update_sidebar_description(selected_value):
    for opt in sidebar_options:
        if opt["value"] == selected_value:
            return opt.get("description", "")
    return ""

# Callback detailview
@app.callback(
    Output('detalhe-view', 'children'),
    Input('vote-table', 'active_cell'),
    State('vote-table', 'data')
)
def show_vote_details(active_cell, table_data):
    if not active_cell or active_cell['column_id'] != 'Vote_ID':
        return ""
    row_idx = active_cell['row']
    vote_id = table_data[row_idx]['Vote_ID']
    filtered = df_detalhe[df_detalhe['Vote_ID'] == vote_id]
    if filtered.empty:
        return ""
    
    row = filtered.iloc[0]
    return html.Div([
        html.Div(
            row["Título"],
            style={
                "fontSize": "12px",
                "fontWeight": "bold",
                "marginBottom": "14px",
                "color": "orange",
                "whiteSpace": "pre-line",
                "wordBreak": "break-word",
                "maxWidth": "600px",
                "lineHeight": "1.5",
                "fontFamily": "Dash Digital-7, monospace"
            }
        ),
        html.Div([
            html.A("🔗", href=row["TextLink"], target="_blank", style={
                "fontSize": "25px",
                "textDecoration": "none",
                "verticalAlign": "middle",
                "fontFamily": "Dash Digital-7, monospace"
            }),
            html.Span([
                html.Span("@ iniciativa nº", style={"fontWeight": "bold", "fontFamily": "Dash Digital-7, monospace"}),
                html.Span(str(row["Iniciative_ID"]), style={"fontFamily": "Dash Digital-7, monospace"})
            ], style={"color": "white", "fontSize": "10px", "fontFamily": "Dash Digital-7, monospace"})
        ], style={
            "display": "flex",
            "justifyContent": "space-between",
            "alignItems": "center",
            "fontFamily": "Dash Digital-7, monospace"
        }),
    ], style={
        "background": "#181818",
        "padding": "15px",
        "borderRadius": "15px",
        "color": "white",
        "maxWidth": "650px",
        "fontFamily": "Dash Digital-7, monospace"
    })

# Callback for visuals (now using the single radio value)
@app.callback(
    [Output('donut_chart_container', 'children'),
     Output('funnel_chart_container', 'children')],
    Input('author_selector_radio', 'value')
)
def update_visuals(selected):
    if not selected or selected.startswith("sep"):
        return no_update, no_update

    filtered_donut = df_donut[df_donut['IniciativasXVI (2).Custom.1'] == selected]
    counts = filtered_donut['IniDescTipo'].value_counts().reset_index()
    counts.columns = ['IniDescTipo', 'Count']

    if counts.empty:
        donut_fig = html.Div(f'Nenhum dado disponível para {selected}',
                             style={'color': 'white', 'background': 'black', 'padding': '5px', 'fontFamily': 'Dash Digital-7, monospace'})
    else:
        total = counts['Count'].sum()
        counts['label_for_legend'] = counts.apply(
            lambda row: f"{row['Count']} {row['IniDescTipo']} ({row['Count'] / total:.1%})",
            axis=1
        )
        fig_donut = px.pie(
            counts,
            names='label_for_legend',
            values='Count',
            hole=0.45,
            title=f'',
            template='plotly_dark',
            color='IniDescTipo',
            color_discrete_map=color_map
        )
        fig_donut.update_traces(
            textinfo='none',
            marker=dict(line=dict(color='black', width=0.5)),
            pull=[0.05]*len(counts),
            showlegend=True,
        )
        fig_donut.update_layout(
            font=dict(family='Dash Digital-7, monospace', color='white', size=11),
            plot_bgcolor='black',
            paper_bgcolor='black',
            margin=dict(t=30, b=30, l=30, r=30),
            height=250,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(color="white", size=8, family='Dash Digital-7, monospace'),
            )
        )
        donut_fig = dcc.Graph(figure=fig_donut, style={"height": "100%", "width": "100%"})

# Funnel chart logic
    filtered_funnel = df_funnel[df_funnel['Quem'] == selected]
    if filtered_funnel.empty:
        # Show your custom message here
        funnel_fig = html.Div(
            "Presidente da Assembleia não propõe leis.",
            style={
                "color": "#f5970a",
                "background": "#222",
                "padding": "40px 10px",
                "textAlign": "center",
                "fontSize": "15px",
                "fontFamily": "Dash Digital-7, monospace",
                "borderRadius": "12px"
            }
        )
    else:
        stage_order = sorted(
            filtered_funnel['Fase n'].unique(),
            key=lambda x: int(x.split('.')[0]),
            reverse=True
        )
        fig_funnel = px.funnel(
            filtered_funnel,
            x='Sum of Iniciativas',
            y='Fase n',
            title=f"",
            category_orders={'Fase n': stage_order},
            template='plotly_dark',
            color_discrete_sequence=blue_shades
        )
        fig_funnel.update_layout(
            font=dict(family='Dash Digital-7, monospace', color='white', size=8),
            plot_bgcolor='black',
            paper_bgcolor='black',
            margin=dict(t=30, b=30, l=30, r=30),
            height=250,
            yaxis=dict(
                title_text='',
                tickangle=0,
                tickson='labels',
                ticks='outside',
                ticklen=10,
                tickfont=dict(color='white', family='Dash Digital-7, monospace'),
                automargin=True,
                side='left'
            )
        )
        funnel_fig = dcc.Graph(figure=fig_funnel, style={"height": "100%", "width": "100%"})

    return donut_fig, funnel_fig

# Callback for table and summaries (update to use selected radio)
@app.callback(
    Output('vote-table', 'data'),
    Output('blocksplit-summary', 'children'),
    Output('unanimous-summary', 'children'),
    Output('approved-summary', 'children'),
    [Input('author_selector_radio', 'value'),
     Input('blocksplit-filter', 'value'),
     Input('unanimous-filter', 'value'),
     Input('approved-filter', 'value')]
)
def update_vote_table_and_summaries(selected_author, blocksplit, unanimous, approved):
    if not selected_author or selected_author.startswith("sep"):
        return [], "", "", ""
    
    dff = df_vote[df_vote['Proposed_By'] == selected_author]
    
    block_split_counts = dff['Block_Or_Split'].value_counts(normalize=True)
    block_pct = round(100 * block_split_counts.get('Block Vote', 0), 1)
    split_pct = round(100 * block_split_counts.get('Split Vote', 0), 1)
    blocksplit_summary = f"\u2764\ufe0f {block_pct}%         \U0001f494 {split_pct}%"

    unanimous_counts = dff['Unanimous_Or_Not'].value_counts(normalize=True)
    unanimous_pct = round(100 * unanimous_counts.get('Unanimous', 0), 1)
    notunanimous_pct = round(100 - unanimous_pct, 1)
    unanimous_summary = f"\U0001F91D {unanimous_pct}%                           \U0001F914 {notunanimous_pct}%"

    approved_counts = dff['Approved_Or_Rejected'].value_counts(normalize=True)
    approved_pct = round(100 * approved_counts.get('Approved', 0), 1)
    rejected_pct = round(100 - approved_pct, 1)
    approved_summary = f"\U0001F44D {approved_pct}%          \U0001F44E {rejected_pct}%"

    if blocksplit or unanimous or approved:
        if blocksplit:
            dff = dff[dff['Block_Or_Split'] == blocksplit]
        if unanimous:
            dff = dff[dff['Unanimous_Or_Not'] == unanimous]
        if approved:
            dff = dff[dff['Approved_Or_Rejected'] == approved]
        data = dff[['Vote_ID', 'Contra', 'Favor', 'Abstenção']].to_dict('records')
    else:
        data = []

    return data, blocksplit_summary, unanimous_summary, approved_summary

if __name__ == '__main__':
    app.run(jupyter_mode="tab")
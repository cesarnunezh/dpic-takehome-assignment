from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from ..data_pipeline.run_queries import run_queries
from .figures import gen_bar_chart_by, create_interactive_bar, create_scatter, gen_bar_chart

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

tables = list(run_queries().values())

district_dropdown = html.Div(
    [
        dbc.Label("Select a District", html_for="district_dropdown"),
        dcc.Dropdown(
            id="district-dropdown",
            options=sorted(tables[-1]["district"].unique()),
            value='Bhubaneswar',
            clearable=False,
            maxHeight=600,
            optionHeight=50
        ),
    ],  className="mb-4",
)

year_dropdown = html.Div(
    [
        dbc.Label("Select Year", html_for="date-checklist"),
        dcc.Dropdown(
            id = "year-dropdown",
            options=list(range(2020,2025)),
            value=2024,
        ),
    ],
    className="mb-4",
)

control_panel = dbc.Card(
    dbc.CardBody(
        [year_dropdown, district_dropdown],
        className="bg-light",
    ),
    className="mb-4"
)

heading = html.H1("Odisha Enrollment and Grievances Analysis",
                  className="bg-secondary text-white p-2 mb-4",
                  style={
                    "padding": "10px",
                    "position": "sticky",  # Make the header sticky
                    "top": 0,
                    "zIndex": 9999}
                    )

about_card = dcc.Markdown(
    """
    This dashboard provides an interactive view of key education and grievance indicators across districts in Odisha 
    from 2020 to 2024. It allows users to explore patterns in student enrollment and grievances reported at Industrial 
    Training Institutes (ITIs), offering insights into regional disparities, trends over time, and the relationship 
    between enrollment levels and reported issues. The goal is to support data-driven decision-making to improve the 
    learning environment across the state.
    """)

data_card = dcc.Markdown(
    """
    This dashboard uses mainly two sources of data:
    - [Enrollments Data](https://github.com/zenbuffy/irishGenderPayGap/tree/main): Contains enrollment numbers for Industrial
    Training Institutes (ITIs) by district and year.
    - [Grievances Data](https://github.com/zenbuffy/irishGenderPayGap/tree/main): Contains citizen complaints related to
    vocational education.

     This site was created for a Take-Home Test application for a Data Science/Engineering Intern position.
    """
)

info = dbc.Accordion([
    dbc.AccordionItem(about_card, title="About the dashboard", ),
    dbc.AccordionItem(data_card, title="Data Source")
],  start_collapsed=True)

text_1 = html.Div([
    html.P("Considering all Odisha's district as a whole, there are some important insights from the data:", style={"marginBottom": "10px"}),
    html.Ul([
        html.Li("Enrollment in Industrial Training Institutes (ITIs) has remained largely constant over the years," +
                "with the exception of 2024, which saw a notable increase to over 1 million students — a 9.6% rise from 2023."),
        html.Li("Grievances have increased compared to 2020 levels. The most common issues are related to utilities, including:"),
        html.Ul([
            html.Li("Irregular water supply"),
            html.Li("Non-working internet"),
            html.Li("Lack of electricity during class hours")
        ])
    ])
])

text_2 = html.Div([
    html.H5("Analyzing missmatch between enrollment and grievances"),
    html.Ul([
       html.Li("Districts with higher enrollments tend to report fewer grievances per 1,000 students."),
        html.Li("There is notable variation in grievance rates across districts, suggesting uneven student experiences."),
        html.Li("Smaller districts could benefit from targeted improvements to student services."),
    ])
], style={'margin': '20px', 'fontFamily': 'Arial', 'fontSize': '15px'})

app.layout = dbc.Container(
    [
        heading,
        dbc.Row([
            dbc.Col(info, md=3),
            dbc.Col([
                html.H2("Summary of Odisha's Enrollment and Grievances"),
                text_1,
                dbc.Row([
                    dbc.Col(html.Div(id="enrollment-gender")),
                    dbc.Col(html.Div(id="grievances-cat"))
                    ]),
                html.Div(text_2),
                dbc.Row([dbc.Col(html.Div(id="grievances-pc")),
                         dbc.Col(html.Div(id="scatter-graph"))])
            ]),
        ]),
        dbc.Row([dbc.Col(control_panel, md=3),
                 dbc.Col([
                     html.H2(id="title-2"),
                     dbc.Row([dbc.Col(html.Div(id="enrollment-card")), dbc.Col(html.Div(id="grievances-card"))]),
                     dbc.Row([dbc.Col(html.Div(id="evol-enrollment")), dbc.Col(html.Div(id="grievances-enrollment"))]),
                     dbc.Row([dbc.Col(html.Div(id="programs-graph")), dbc.Col(html.Div(id="cat-grievances-graph"))])])
                ], className="my-4")
    ],
    fluid=True,
)

@callback(
    Output("enrollment-card", "children"),
    Input("year-dropdown", "value"),
    Input("district-dropdown", "value")
)
def make_card_enrollment(selected_year, selected_district):
    data = tables[-1]
    data = data[(data["year"] == selected_year) & (data["district"] == selected_district)]
    enrollment_data = data.groupby(["year", "district"])["enrollment"].sum().reset_index()
    n_enrolled = enrollment_data.loc[0,"enrollment"]
    n_programs = len(data["program"].unique())

    enrollment = dbc.Alert(dcc.Markdown(
        f"""
        **Total Enrollment**: {int(n_enrolled):,} \n
        **Number of Programs** : {n_programs}
        """,
    ))

    card =  dbc.Card([
        dbc.CardHeader(html.H4(f"Enrollment summary"), className="text-center"),
        dbc.CardBody(enrollment)
    ])
    return card

@callback(
    Output("grievances-card", "children"),
    Input("year-dropdown", "value"),
    Input("district-dropdown", "value")
)
def make_card_grievances(selected_year, selected_district):
    data = tables[-2]
    data = data[(data["year"] == selected_year) & (data["district_name"] == selected_district)]
    grievances_data = data.groupby(["year", "district_name"])["num_grievances"].sum().reset_index()
    n_grievances = grievances_data.loc[0,"num_grievances"]
    n_types = len(data["cat_grivance"].unique())

    enrollment = dbc.Alert(dcc.Markdown(
        f"""
        **Total Grievances**: {int(n_grievances):,} \n
        **Types of Grievances** : {n_types}
        """,
    ))

    card =  dbc.Card([
        dbc.CardHeader(html.H4(f"Grievances summary"), className="text-center"),
        dbc.CardBody(enrollment)
    ])
    return card


@callback(
    Output("enrollment-gender", "children"),
    Output("grievances-cat", "children"),
    Output("grievances-pc", "children"),
    Output("scatter-graph", "children"),
    Output("programs-graph", "children"),
    Output("cat-grievances-graph", "children"),
    Output("evol-enrollment", "children"),
    Output("grievances-enrollment", "children"),
    Output("title-2", "children"),
    Input("year-dropdown", "value"),
    Input("district-dropdown", "value")
)
def update_charts(selected_year, selected_district):
    
    labels_dict = {'year' : 'Year',
                   'enrollment' : "Annual Enrollment",
                   'gender' : "Gender",
                   'num_grievances' : "Number of Grievances",
                   'cat_grivance' : "Type of Grievance",
                   'district' : "District Name",
                   'grievances_pc' : 'Grievances per 1,000 students',
                   'program' : "Program Name"}
    enrollment_gender = gen_bar_chart_by(tables[0], x_var = "year", y_var ="enrollment",
                                         by_var = "gender", title = "Evolution of Enrollment by Gender",
                                         labels = labels_dict)
    grievances_cat = gen_bar_chart_by(tables[1], x_var = "year", y_var ="num_grievances",
                                      by_var = "cat_grivance", title = "Evolution of Grievances by Type",
                                      labels = labels_dict)
    grievances_pc = create_interactive_bar(tables[2], selected_year = selected_year, selected_district = None,
                                           x_var = "grievances_pc", y_var = "district", labels = labels_dict, 
                                           title = "Number of Grievances per 1,000 students by Districts",
                                           fmt = ".2f")
    scatter = create_scatter(tables[2], x_var = 'enrollment', y_var = 'grievances_pc', labels = labels_dict,
                             title = "Relationship Between Enrollment and Grievances 2020 - 2024")
    programs_graph = create_interactive_bar(tables[5], selected_year = selected_year, selected_district = selected_district,
                                           x_var = "enrollment", y_var = "program", labels = labels_dict, 
                                           title = f"Enrollment by Program in {selected_district}, {selected_year}",
                                           fmt = ",")
    cat_grievances_graph = create_interactive_bar(tables[4], selected_year = selected_year, selected_district = selected_district,
                                           x_var = "num_grievances", y_var = "cat_grivance", labels = labels_dict, 
                                           title = f"Number of Grievances by Type in {selected_district}, {selected_year}",
                                           fmt = ",")
    enrollment_dist = gen_bar_chart(tables[5], x_var = "year", y_var = "enrollment", selected_district = selected_district,
                                    title = f"Evolution of Enrollment in {selected_district}", labels=labels_dict)
    grievances_dist = gen_bar_chart(tables[4], x_var = "year", y_var = "num_grievances", selected_district = selected_district,
                                    title = f"Evolution of Grievances in {selected_district}", labels=labels_dict)
    title_2 = f"Summary of {selected_district} Enrollment and Grievances in {selected_year}"

    return (
        html.Iframe(
            srcDoc = enrollment_gender.to_html(),
            style={"width": "100%", "height": "300px", "border": "0"},
        ),
        html.Iframe(
            srcDoc = grievances_cat.to_html(),
            style={"width": "100%", "height": "300px", "border": "0"},
        ),
        html.Iframe(
            srcDoc = grievances_pc.to_html(),
            style={"width": "100%", "height": "300px", "border": "0",
                   "alignItems": "center"},
        ),
        html.Iframe(
            srcDoc = scatter.to_html(),
            style={"width": "100%", "height": "300px", "border": "0",
                   "alignItems": "center"},
        ),
        html.Iframe(
            srcDoc = programs_graph.to_html(),
            style={"width": "100%", "height": "300px", "border": "0"},
        ),
        html.Iframe(
            srcDoc = cat_grievances_graph.to_html(),
            style={"width": "100%", "height": "300px", "border": "0"},
        ),
        html.Iframe(
            srcDoc = enrollment_dist.to_html(),
            style={"width": "100%", "height": "300px", "border": "0"},
        ),
        html.Iframe(
            srcDoc = grievances_dist.to_html(),
            style={"width": "100%", "height": "300px", "border": "0"},
        ),        
        title_2
    )

def main():
    app.run(debug=False)

if __name__ == "__main__":
    main()
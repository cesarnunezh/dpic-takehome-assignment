import altair as alt
import pandas as pd

def gen_bar_chart_by(df: pd.DataFrame, x_var: str, y_var: str, by_var: str,
                     title: str, labels: dict) -> alt.Chart:
    '''
    Function to create a bar chart colored by a specific variable
    '''
    # color_scale = alt.Scale(domain=["Female", "Male", "Other"], range=["#005A9C", "#A8D0E6", "#A8F0F6"])
    
    by_selection = alt.selection_point(fields=[by_var], bind="legend")
    bar = alt.Chart(df).mark_bar().encode(
        x = alt.X(
            f"{x_var}:N",
            axis = alt.Axis(title = "Year", titleFontSize=14, labelFontSize=12)
        ),
        y = f'{y_var}',
        color = alt.Color(f"{by_var}:N"),
        opacity=alt.condition(by_selection, alt.value(0.9), alt.value(0.2)),
        tooltip = [
            alt.Tooltip(f"{x_var}", title =labels[x_var]),
            alt.Tooltip(f"{y_var}:Q", title=labels[y_var], format = ","),
            alt.Tooltip(f"{by_var}", title=labels[by_var]),
        ]
    ).add_params(by_selection).properties(
        width=350,  #  Increase width
        height=200,  # Increase height
        title=title,
    )

    return bar

def create_interactive_bar(df: pd.DataFrame, selected_year: int, selected_district: int | None,
                           x_var: str, y_var: str, labels: dict, title: str, fmt: str):

    select = alt.selection_point(name="select", on="click")
    highlight = alt.selection_point(name="highlight", on="pointerover", empty=False)
    stroke_width = (
        alt.when(select)
        .then(alt.value(2, empty=False))
        .when(highlight)
        .then(alt.value(1))
        .otherwise(alt.value(0))
    )

    df = df[df["year"] == selected_year]
    if selected_district is not None:
        if "district" in df.columns:
            df = df[df["district"] == selected_district]
        else:
            df = df[df["district_name"] == selected_district]
    
    bar = (
        alt.Chart(df)
        .mark_bar(stroke="black", cursor="pointer")
        .encode(
            y=alt.Y(
                f"{y_var}:N",
                axis=alt.Axis(title=labels[y_var], titleFontSize=14, labelFontSize=12),
                sort=alt.EncodingSortField(
                    field=f"{x_var}", op="sum", order="descending"
                ),
            ),
            x=alt.X(
                f"{x_var}:Q",
                axis=alt.Axis(title=labels[x_var], titleFontSize=14, labelFontSize=12),
            ),
            opacity=alt.condition(select, alt.value(1), alt.value(0.3)),
            tooltip = [
                alt.Tooltip(f"{x_var}:Q", title =labels[x_var]),
                alt.Tooltip(f"{y_var}", title=labels[y_var]),
            ],
            strokeWidth=stroke_width,
        )
    )

    avg_line = alt.Chart(df).mark_rule(color="red", strokeDash=[5, 5]).encode(
        x=alt.X(f"mean({x_var}):Q", title=labels[x_var]),
        size=alt.value(2),
        tooltip=[alt.Tooltip(f"mean({x_var}):Q", title=f"Avg {labels[x_var]}", format=fmt)]
    )

    text = bar.mark_text(
        align='left',
        baseline='middle',
        dx=3  # space between bar and text
    ).encode(
        text=alt.Text(f"{x_var}:Q", format=fmt),
        opacity=alt.condition(select, alt.value(1), alt.value(0.3)),
    )

    final_bar = (bar + avg_line + text).properties(
            title=title,
            width=300,
            height=200,  
        ).add_params(select, highlight)

    return final_bar

def create_scatter(df: pd.DataFrame, x_var: str, y_var: str, labels: dict,
                   title: str):
    
    x_min, x_max = df[x_var].min(), df[x_var].max()
    y_min, y_max = df[y_var].min(), df[y_var].max()

    district_selection = alt.selection_point(fields=["district"], bind="legend")
    scatter = alt.Chart(df).mark_circle(size=100).encode(
        x=alt.X(
            f"{x_var}:Q", 
            axis=alt.Axis(title=labels[x_var], titleFontSize=14, labelFontSize=12), 
            scale=alt.Scale(domain=[x_min*0.9, x_max*1.1])),
        y=alt.Y(
            f"{y_var}:Q", 
            axis=alt.Axis(title=labels[y_var], titleFontSize=14, labelFontSize=12),
            scale=alt.Scale(domain=[y_min*0.9, y_max*1.1])),
        color=alt.Color("district:N", title=labels["district"]),
        opacity=alt.condition(district_selection, alt.value(1), alt.value(0.1)),
        tooltip=[                
            alt.Tooltip("district:N", title=labels["district"]),
            alt.Tooltip("year:N", title=labels["year"]),
            alt.Tooltip(f"{x_var}:Q", title =labels[x_var], format= ","),
            alt.Tooltip(f"{y_var}:Q", title=labels[y_var], format= ","),
            ]
    ).add_params(district_selection)

    regression = alt.Chart(df).transform_filter(
        district_selection
    ).transform_regression(
        x_var, y_var
    ).mark_line(size=2, color='black').encode(
        x=f"{x_var}:Q",
        y=f"{y_var}:Q",
        opacity=alt.condition(district_selection, alt.value(1), alt.value(0)),
    )

    chart = (scatter + regression).properties(
        title=title,
        width=350,
        height=200
    )
    return chart

def gen_bar_chart(df: pd.DataFrame, x_var: str, y_var: str, selected_district: str,
                  title: str, labels: dict) -> alt.Chart:
    '''
    Function to create a bar chart 
    '''
    # color_scale = alt.Scale(domain=["Female", "Male", "Other"], range=["#005A9C", "#A8D0E6", "#A8F0F6"])
    
    if "district" in df.columns:
        df = df[df["district"] == selected_district]
        df = df.groupby(['year', 'district'])[y_var].sum().reset_index()
    else:
        df = df[df["district_name"] == selected_district]
        df = df.groupby(['year', 'district_name'])[y_var].sum().reset_index()

    bar = alt.Chart(df).mark_bar().encode(
        x = alt.X(
            f"{x_var}:N",
            axis = alt.Axis(title = "Year", titleFontSize=14, labelFontSize=12)
        ),
        y = f'{y_var}',
        tooltip = [
            alt.Tooltip(f"{x_var}", title =labels[x_var]),
            alt.Tooltip(f"{y_var}:Q", title=labels[y_var], format = ","),
        ]
    ).properties(
        width=350,  #  Increase width
        height=200,  # Increase height
        title=title,
    )

    return bar
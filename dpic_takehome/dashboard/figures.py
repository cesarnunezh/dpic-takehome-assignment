import altair as alt

def bar_chart_by_gender(df):

    color_scale = alt.Scale(domain=["Female", "Male", "Other"], range=["#005A9C", "#A8D0E6", "#A8F0F6"])

    gender_selection = alt.selection_point(fields=["gender"], bind="legend")

    bar = alt.Chart(df).mark_bar().encode(
        x = alt.X(
            "enrollment:Q",
            stack = "zero",
            axis = alt.Axis(title = "Annual Enrollment", titleFontSize=14, labelFontSize=12)
        ),
        y = alt.Y("gender:Q", sort = ["Female", "Male", "Other"], title = ""),
        color = alt.Color("gender:N", scale = color_scale, title = "Gender"),
        opacity = alt.condition(gender_selection, alt.value(0.9), alt.value(0.2)),
        tooltip = [
            alt.Tooltip("year", title ="Year"),
            alt.Tooltip("gender", title="Gender"),
            alt.Tooltip("enrollment", title="Annual Enrollment"),
        ]
    ).add_params(gender_selection).properties(
        width=500,  #  Increase width
        height=100,  # Increase height
        title="Gender",
    )

    return bar
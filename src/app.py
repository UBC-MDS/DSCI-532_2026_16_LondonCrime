from shiny import App, render, ui, reactive
import plotly.express as px
# from ridgeplot import ridgeplot
# import seaborn as sns
from shinywidgets import render_plotly, output_widget
import pandas as pd

data = pd.read_csv("data/raw/LondonCrimeData.csv")

BOROUGHS = sorted(['Barking and Dagenham', 'Waltham Forest', 'Tower Hamlets', 'Sutton', 'Southwark', 'Richmond upon Thames', 'Redbridge', 'Newham', 'Merton', 'Lewisham', 'Lambeth', 'Kingston upon Thames', 'Kensington and Chelsea', 'Islington', 'Hounslow', 'Wandsworth', 'Hillingdon', 'Harrow', 'Haringey', 'Hammersmith and Fulham', 'Hackney', 'Greenwich', 'Enfield', 'Ealing', 'Croydon', 'City of London', 'Camden', 'Bromley', 'Brent', 'Bexley', 'Barnet', 'Havering', 'Westminster'])

CRIME_TYPES = [
    "Theft and Handling",
    "Criminal Damage",
    "Robbery",
    "Drugs",
    "Violence Against the Person",
    "Other Notifiable Offences",
    "Sexual Offences",
    "Fraud or Forgery",
    "Burglary"
]

# Asked Claude to generate a color palette dictionary for the 6 crime types
# and to create CSS code to ensure instances (plots, text boxes) use the same colorings.
CRIME_COLORS = {
    "Theft and Handling":          "#4E79A7",
    "Criminal Damage":             "#F28E2B",
    "Robbery":                     "#E15759",
    "Drugs":                       "#76B7B2",
    "Violence Against the Person": "#59A14F",
    "Other Notifiable Offences":   "#B07AA1",
    "Sexual Offences":             "#FF9DA7",
    "Fraud or Forgery":            "#9C755F",
    "Burglary":                    "#EDC948",
}
# CSS block that maps each crime type to its color for value box highlight, obtained from Claude (see above).
CRIME_CSS = "\n".join(
    f'.crime-color-{i} {{ color: {color} !important; font-weight: bold; }}'
    for i, color in enumerate(CRIME_COLORS.values())
)
CRIME_COLOR_INDEX = {name: i for i, name in enumerate(CRIME_COLORS.keys())}

app_ui = ui.page_fillable(
    ui.panel_title("Crime in London"),
    # Asked Claude for CSS styling to make the year labels smaller and the numbers larger in the text boxes.
    ui.tags.style(f"""
        #total_crimes {{ font-size: 2rem; font-weight: bold; }}
        #crime_rate {{ font-size: 2rem; font-weight: bold; }}
        #year_label_1, #year_label_2, #year_label_3, #year_label_4 {{ font-size: 0.8rem; opacity: 0.7; }}
        .crime-value {{ font-size: 1.5rem; font-weight: bold; display: block; }}
        .crime-label {{ font-size: 0.8rem; opacity: 0.7; display: block; margin-top: 0.5rem; }}
        {CRIME_CSS}
    """),
    # Create sidebar
    ui.layout_sidebar(
        ui.sidebar(
            # Year Selector
            ui.input_slider("year_range", 
                            "Year Range", 
                            min=data.year.min(), 
                            max=data.year.max(), 
                            value=[data.year.min(), data.year.max()], sep=""
                            ),
            # Crime Type Checkbox with Custom Coloring
            ui.tags.div(
                ui.tags.label("Crime Types", style="font-weight: bold; display: block; margin-bottom: 0.5rem;"),
                # Asked Claude to generate the code to color the checkboxes to match the global crime type colors dictionary. Copied code from Claude and replaced placeholder values (such as name).
                ui.tags.div(
                    *[
                        ui.tags.div(
                            ui.tags.input(
                                type="checkbox",
                                name="major_category",
                                value=crime,
                                checked="checked",
                                id=f"major_category_{i}",
                                style=f"margin-right: 0.4rem; accent-color: {CRIME_COLORS[crime]}; color: white;",
                            ),
                            ui.tags.label(
                                crime,
                                **{"for": f"major_category_{i}"},
                                style=f"color: {CRIME_COLORS[crime]}; font-weight: 600; cursor: pointer;",
                            ),
                            style="display: flex; align-items: center; margin-bottom: 0.3rem;",
                        )
                        for i, crime in enumerate(CRIME_TYPES)
                    ],
                    id="major_category",
                    class_="shiny-input-checkboxgroup",
                ),
            ),
            # Borough Multi-Selector with Searching
            ui.input_selectize(  
                "borough",  
                "Select Borough(s):",
                choices=BOROUGHS,
                multiple=True,  
            ),  
            ui.input_action_button("reset_filter", "Clear Filters"),
            open="desktop",
        ),
    # Summary Info Text Boxes
    ui.layout_columns(
        ui.value_box(
            "Total Crimes in London", 
            ui.output_text("year_label_1"), 
            ui.tags.div(
                ui.tags.div(ui.output_text("total_crimes"), class_="crime-value"),
                ui.tags.span("crimes", style="font-size: 0.8rem; opacity: 0.7;"),
            ),
            ),
        ui.value_box(
            "Average Monthly Crime Rate in London", 
            ui.output_text("year_label_2"), 
            ui.tags.div(
                ui.tags.div(ui.output_text("crime_rate"), class_="crime-value"),
                ui.tags.span("crimes per month", style="font-size: 0.8rem; opacity: 0.7;"),
            ),
            ),
        ui.value_box(
            "Max/Min Crime in London - Type",
            ui.output_text("year_label_3"),
            ui.tags.div(
                ui.tags.span("Most Common Crime", class_="crime-label"),
                ui.tags.div(ui.output_ui("most_common_crime"), class_="crime-value"),
                ui.tags.span("Least Common Crime", class_="crime-label"),
                ui.tags.div(ui.output_ui("least_common_crime"), class_="crime-value"),
            ),
        ),
        ui.value_box(
            "Max/Min Crime in London - Borough",
            ui.output_text("year_label_4"),
            ui.tags.div(
                ui.tags.span("Highest Amount of Crime", class_="crime-label"),
                ui.tags.div(ui.output_text("highest_crime_borough"), class_="crime-value"),
                ui.tags.span("Lowest Amount of Crime", class_="crime-label"),
                ui.tags.div(ui.output_text("lowest_crime_borough"), class_="crime-value"),
            ),
        ),
        fill=False,
    ),
    # Plots
    ui.layout_columns(
        ui.card(
            output_widget("borough_trend"),
            full_screen=True,
        ),
        ui.card(
            output_widget("crime_type_counts"),
            full_screen=True,
        ),
        ui.card(
            output_widget("crime_type_trend"),
            full_screen=True,
        ),
    ),
    ui.layout_columns(
        ui.card(
            output_widget("crime_type_month_heatmap"),     
            full_screen=True,
        ),
        ui.card(
            output_widget("borough_month_heatmap"),
            full_screen=True,
        ),
    ),
    ),
)

# Code provided by Claude to ensure every plot has the same ordering of colors for the different crime types, created in conjunction with the CRIME_COLORS dictionary and CRIME_CSS.
def apply_crime_colors(fig, color_col="major_category"):
    """Update traces so each crime type uses the consistent palette."""
    for trace in fig.data:
        name = trace.name
        if name in CRIME_COLORS:
            trace.marker.color = CRIME_COLORS[name]
            if hasattr(trace, "line"):
                trace.line.color = CRIME_COLORS[name]
    return fig

def server(input, output, session):
    @reactive.calc
    def filtered_data():
        year = data.year.between(
            left=input.year_range()[0],
            right=input.year_range()[1],
            inclusive="both",
        )
        major_category = data.major_category.isin(input.major_category())
        borough = data.borough.isin(input.borough())
        data_filtered = data[borough & major_category & year]
        return data_filtered
    
    @reactive.calc
    def filtered_data_year():
        year = data.year.between(
            left=input.year_range()[0],
            right=input.year_range()[1],
            inclusive="both",
        )
        data_filtered = data[year]
        return data_filtered
    
    @render.text
    def total_crimes():
        df = filtered_data_year()
        if df.empty:
            return "No Data"
        return str(filtered_data_year().shape[0])

    # Asked Claude to color the text entry by the associated global crime type color.
    @render.ui
    def most_common_crime():
        df = filtered_data_year()
        if df.empty:
            return "No Data"
        crime = str(filtered_data_year().major_category.value_counts().idxmax())
        idx = CRIME_COLOR_INDEX.get(crime, 0)
        return ui.tags.span(crime, class_=f"crime-color-{idx}")

    @render.ui
    def least_common_crime():
        df = filtered_data_year()
        if df.empty:
            return ui.tags.span("No Data")
        crime = str(df.major_category.value_counts().idxmin())
        idx = CRIME_COLOR_INDEX.get(crime, 0)
        return ui.tags.span(crime, class_=f"crime-color-{idx}")

    @render.text
    def highest_crime_borough():
        df = filtered_data_year()
        if df.empty:
            return "No Data"
        return str(df.borough.value_counts().idxmax())

    @render.text
    def lowest_crime_borough():
        df = filtered_data_year()
        if df.empty:
            return "No Data"
        return str(filtered_data_year().borough.value_counts().idxmin())
    
    @render.text
    def crime_rate():
        df = filtered_data_year()
        if df.empty:
            return "No Data"
        monthly_crimes = filtered_data_year().groupby(["year", "month"]).size()
        return str(round(monthly_crimes.mean()))
    
    # Create a function for calculating the year label
    def year_label():
        start, end = input.year_range()
        if start == end:
            return str(start)
        else:
            return f"{start} - {end}"
    
    # Need to have 4 seperate functions for the 4 separate cards: when I try to do all 4 with the same function it gives me errors about duplicates.
    @render.text
    def year_label_1():
        return year_label()
    
    @render.text
    def year_label_2():
        return year_label()

    @render.text
    def year_label_3():
        return year_label()
    
    @render.text
    def year_label_4():
        return year_label()
    
    # Borough trend plot
    @render_plotly
    def borough_trend():
        df = filtered_data()
        if df.empty:
            return px.line(title="No data - select a borough")
        
        df_grouped = df.groupby(["borough", "major_category"]).size().reset_index(name="count")
        df_grouped = df_grouped.sort_values("count", ascending=False)
        
        fig = px.bar(
            df_grouped,
            x="borough",
            y="count",
            color="major_category",
            barmode="stack",
            title="Amount of Crime by Borough and Type",
            labels={"borough": "Borough", "count": "Number of Crimes", "major_category": "Crime Type"},
            color_discrete_map=CRIME_COLORS,
        )
        return fig
    
    # Crime type trend plot
    @render_plotly
    def crime_type_trend():
        df = filtered_data()
        if df.empty:
            return px.line(title="No data - select a borough")
        
        df_grouped = df.groupby(["year", "month", "major_category"]).size().reset_index(name="count")
        df_grouped["date"] = pd.to_datetime(df_grouped[["year", "month"]].assign(day=1))
        
        fig = px.line(
            df_grouped,
            x="date",
            y="count",
            color="major_category",
            title="Amount of Crime by Type Over Time",
            labels={"date": "Date", "count": "Number of Crimes", "major_category": "Crime Type"},
            color_discrete_map=CRIME_COLORS,
        )
        return fig

    # Crime type counts plot
    @render_plotly
    def crime_type_counts():
        df = filtered_data()
        if df.empty:
            return px.bar(title="No data - select a borough")
        
        df_grouped = df.groupby(["major_category"]).size().reset_index(name="count")
        df_grouped = df_grouped.sort_values(["count"], ascending=[True])
        
        fig = px.bar(
            df_grouped,
            x="major_category",
            y="count",
            color="major_category",
            title="Amount of Crime by Type",
            labels={"count": "Number of Crimes", "major_category": "Crime Type"},
            color_discrete_map=CRIME_COLORS,
        )
        return fig
    
    # Crime type v. month
    @render_plotly
    def crime_type_month_heatmap():
        df = filtered_data()
        if df.empty:
            return px.bar(title="No data - select a borough")

        df_grouped = df.groupby(["major_category", "month"]).size().reset_index(name="count")
        df_pivot = df_grouped.pivot(index="major_category", columns="month", values="count")
        df_pivot = df_pivot.div(df_pivot.sum(axis=1), axis=0) * 100

        fig = px.imshow(
            df_pivot,
            title="Crime by Type and Month (% of Type Total)",
            labels={"x": "Month", "y": "Crime Type", "color": "% of Type Total"},
            color_continuous_scale="Viridis_r",
        )
        return fig
    
    # Borough v. monthe heatmap
    @render_plotly
    def borough_month_heatmap():
        df = filtered_data()
        if df.empty:
            return px.imshow([[]], title="No data - select a borough")

        df_grouped = df.groupby(["borough", "month"]).size().reset_index(name="count")
        df_pivot = df_grouped.pivot(index="borough", columns="month", values="count")
        df_pivot = df_pivot.div(df_pivot.sum(axis=1), axis=0) * 100

        fig = px.imshow(
            df_pivot,
            title="Crime by Borough and Month (% of Borough Total)",
            labels={"x": "Month", "y": "Borough", "color": "% of Borough Total"},
            color_continuous_scale="Viridis_r",
            aspect="auto",
        )
        return fig

    # Reset Filters Button
    @reactive.effect
    @reactive.event(input.reset_filter)
    def reset_filters():
        ui.update_slider("year_range", value=[int(data.year.min()), int(data.year.max())])
        ui.update_checkbox_group("major_category", selected=[
            "Theft and Handling", "Criminal Damage", "Robbery",
            "Drugs", "Violence Against the Person", "Other Notifiable Offences"
        ])
        ui.update_selectize("borough", selected=[])

app = App(app_ui, server)
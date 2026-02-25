from shiny import App, render, ui, reactive
import plotly.express as px
# from ridgeplot import ridgeplot
# import seaborn as sns
from shinywidgets import render_plotly, render_widget, output_widget
import pandas as pd

data = pd.read_csv("data/raw/LondonCrimeData.csv")

boroughs = sorted(['Barking and Dagenham', 'Waltham Forest', 'Tower Hamlets', 'Sutton', 'Southwark', 'Richmond upon Thames', 'Redbridge', 'Newham', 'Merton', 'Lewisham', 'Lambeth', 'Kingston upon Thames', 'Kensington and Chelsea', 'Islington', 'Hounslow', 'Wandsworth', 'Hillingdon', 'Harrow', 'Haringey', 'Hammersmith and Fulham', 'Hackney', 'Greenwich', 'Enfield', 'Ealing', 'Croydon', 'City of London', 'Camden', 'Bromley', 'Brent', 'Bexley', 'Barnet', 'Havering', 'Westminster'])

app_ui = ui.page_fillable(
    ui.panel_title("Crime in London"),
    ui.tags.style("""
        #total_crimes { font-size: 2rem; font-weight: bold; }
        #crime_rate { font-size: 2rem; font-weight: bold; }
        #most_common_crime { font-size: 2rem; font-weight: bold; }
        #lowest_crime_borough { font-size: 2rem; font-weight: bold; }
        #year_label_1, #year_label_2, #year_label_3, #year_label_4 { font-size: 0.8rem; opacity: 0.7; }
    """),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_slider("year_range", "Year Range", min=data.year.min(), max=data.year.max(), value=[data.year.min(), data.year.max()], sep=""),
            ui.input_checkbox_group(
                id="major_category",
                label="Crime Types",
                choices=[
                    "Theft and Handling",
                    "Criminal Damage",
                    "Robbery",
                    "Drugs",
                    "Violence Against the Person",
                    "Other Notifiable Offences"
                ],
                selected=[
                    "Theft and Handling",
                    "Criminal Damage",
                    "Robbery",
                    "Drugs",
                    "Violence Against the Person",
                    "Other Notifiable Offences"
                ],
            ),
            ui.input_selectize(  
                "borough",  
                "Select Borough(s):",
                choices=boroughs,
                multiple=True,  
            ),  
            ui.input_action_button("reset_filter", "Reset filter"),
            open="desktop",
        ),
    ui.layout_columns(
        ui.value_box(
            "Total Crimes in London", 
            ui.output_text("year_label_1"), 
            ui.output_text("total_crimes")
            ),
        ui.value_box(
            "Average Monthly Crime Rate in London", 
            ui.output_text("year_label_2"), 
            ui.output_text("crime_rate")
            ),
        ui.value_box(
            "Most Common Crime in London", 
            ui.output_text("year_label_3"), 
            ui.output_text("most_common_crime")
            ),
        ui.value_box(
            "Lowest Crime Borough in London", 
            ui.output_text("year_label_4"), 
            ui.output_text("lowest_crime_borough")
            ),
        fill=False,
    ),
    ui.layout_columns(
        ui.card(
            ui.card_header("Amount of Crime - Borough Trend Comparison"),
            output_widget("borough_trend"),
            full_screen=True,
        ),
        ui.card(
            ui.card_header("Amount of Crime by Type"),
            output_widget("crime_type_counts"),
            full_screen=True,
        ),
        ui.card(
            ui.card_header("Amount of Crime - Type Trend Comparison"),
            output_widget("crime_type_trend"),
            full_screen=True,
        ),
    ),
    ui.layout_columns(
        ui.card(
            ui.card_header("Crime Heatmap by Borough and Month"),
            output_widget("crime_heatmap"),     
            full_screen=True,
        ),
        ui.card(
            ui.card_header("Recent Incidents"),
            ui.p("list of most recent incidents"),
            full_screen=True,
        ),
    ),
    ),
)

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
        # df = filtered_data()
        # if df.empty:
        #     return "No Data"
        # return str(df.shape[0])
        return str(filtered_data_year().shape[0])

    
    @render.text
    def most_common_crime():
        # df = filtered_data()
        # if df.empty:
        #     return "No Data"
        # return str(df.major_category.value_counts().idxmax())
        return str(filtered_data_year().major_category.value_counts().idxmax())

    
    @render.text
    def lowest_crime_borough():
        # df = filtered_data()
        # if df.empty:
        #     return "No Data"
        # return str(df.borough.value_counts().idxmin())
        return str(filtered_data_year().borough.value_counts().idxmin())
    
    @render.text
    def crime_rate():
        # df = filtered_data()
        # if df.empty:
        #     return "No data"
        # monthly_crimes = df.groupby(["year", "month"]).size()
        # return str(round(monthly_crimes.mean()))
    
        monthly_crimes = filtered_data_year().groupby(["year", "month"]).size()
        return str(round(monthly_crimes.mean()))
    
    def year_label():
        start, end = input.year_range()
        if start == end:
            return str(start)
        else:
            return f"{start} - {end}"
    
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
    
    @render_plotly
    def borough_trend():
        df = filtered_data()
        if df.empty:
            return px.line(title="No data available")
        
        df_grouped = df.groupby(["year", "month", "borough"]).size().reset_index(name="count")
        df_grouped["date"] = pd.to_datetime(df_grouped[["year", "month"]].assign(day=1))
        
        fig = px.line(
            df_grouped,
            x="date",
            y="count",
            color="borough",
            title="Amount of Crime by Borough Over Time",
            labels={"date": "Date", "count": "Number of Crimes", "borough": "Borough"},
        )
        return fig
    
    @render_plotly
    def crime_type_trend():
        df = filtered_data()
        if df.empty:
            return px.line(title="No data available")
        
        df_grouped = df.groupby(["year", "month", "major_category"]).size().reset_index(name="count")
        df_grouped["date"] = pd.to_datetime(df_grouped[["year", "month"]].assign(day=1))
        
        fig = px.line(
            df_grouped,
            x="date",
            y="count",
            color="major_category",
            title="Amount of Crime by Type Over Time",
            labels={"date": "Date", "count": "Number of Crimes", "major_category": "Crime Type"},
        )
        return fig

    @render_plotly
    def crime_type_counts():
        df = filtered_data()
        if df.empty:
            return px.bar(title="No data available")
        
        df_grouped = df.groupby(["year", "major_category"]).size().reset_index(name="count")
        df_grouped = df_grouped.sort_values(["year", "count"], ascending=[True, True])
        
        fig = px.bar(
            df_grouped,
            x="year",
            y="count",
            color="major_category",
            barmode="group",
            title="Amount of Crime by Type Per Year",
            labels={"year": "Year", "count": "Number of Crimes", "major_category": "Crime Type"},
        )
        return fig
    
    @render_plotly
    def crime_heatmap():
        df = filtered_data()
        if df.empty:
            return px.bar(title="No data available")
        
        df_grouped = df.groupby(["borough", "month"]).size().reset_index(name="count")
        df_pivot = df_grouped.pivot(index="borough", columns="month", values="count")
        
        fig = px.imshow(
            df_pivot,
            title="Crime by Borough and Month",
            labels={"x": "Month", "y": "Borough", "color": "Number of Crimes"},
            color_continuous_scale="Cividis",
        )
        return fig

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
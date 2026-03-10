import pandas as pd

def filtered_data(data, year_range, major_categories, boroughs):
    year = data.year.between(year_range[0], year_range[1], inclusive="both")
    major_category = data.major_category.isin(major_categories)
    borough = data.borough.isin(boroughs)
    return data[borough & major_category & year]

def filtered_data_year(data, year_range, major_categories):
    year = data.year.between(year_range[0], year_range[1], inclusive="both")
    major_category = data.major_category.isin(major_categories)
    return data[year & major_category]

def total_crimes(data, year_range, major_categories):
    df = filtered_data_year(data, year_range, major_categories)
    if df.empty:
        return "No Data"
    return str(df.shape[0])
## Updated Job Stories

| Job Story | Status | Notes |
|-----------|--------|-------|
| My family and I are from the United States and we want to visit London for a summer trip. We have two kids under the age of five and we want to make sure our hotel is in a safe and quiet neighborhood. We want to make sure the location of our hotel has the lowest crime rate across all boroughs of London. | Complete ✅ | Need the box at the top right of the dashboard to show the borough with the lowest crime rate. |
| I have recently moved from Barcelona, Spain to London. I work at home and want to ensure the borough I move into has the lowest crime rate. This would ensure that I could safely stay home, and not worry about any solicitors and intruders, especially at night. | Complete ✅ | Need the box at the top right of the dashboard to show the borough with the lowest crime rate. |
| I work at a law firm, and our client was robbed of his possessions in Barnet, a borough in London. The defense argues that no crimes have occurred in that borough for the past two years. Using this dashboard, we can quickly validate or disprove this claim. | Complete ✅ | Need to make sure the heat map shows each borough and how many crimes have taken place there in the past several years. |

---

## Component Inventory

| ID | Type | Shiny widget / renderer | Depends on | Job story |
|----|------|-------------------------|------------|-----------|
| filtered_year | Reactive calculation | @reactive.calc | input_year | #1, #2 |
| filtered_df | Reactive calculation | @reactive.calc | input_year, input_region, input_borough | #3 |
| filtered_region | Reactive calculation | @reactive.calc | input_region | #3 |
| safest_borough | Output | @render.text | filtered_df | #1, #2 |
| input_borough | Input | ui.input_text | NA | #1, #2, #3 |
| heatmap_totalcrime | Output | @render.plot | filtered_df | #3 |

### Reactivity Diagram

`@reactive.calc`

``` mermaid
flowchart TD
  Y[/input_year/]
  R[/input_region/]
  B[/input_borough/]

  Y --> FY{{filtered_year}}
  R --> FR{{filtered_region}}
  B --> FD{{filtered_df}}

  FY --> FD
  FR --> FD

  FY --> FN{{common_crime_type}}
  FY --> FL{{total_crimes}}
  FY --> FK{{crime_rate}}
  FY --> FZ{{safest_borough}}
  FY --> FT{{least_safe_borough}}
  FY --> FJ{{least_common_crime}}

  FD --> O1([safest_borough])
  FD --> O2([heatmap_totalcrime])
```

### Calculation Details

`filtered_year`:

**Depends on:** `input_year`

**Does:** filters the dataset to show the selected year, or range of years

**Consumed by:** `filtered_df`

`filtered_region`:

**Depends on:** `input_region`

**Does:** filters the dataset to show the selected region(s)

**Consumed by:** `filtered_df`

`filtered_df`:

**Depends on:** `input_year` , `input_region`, `input_borough`

**Does:** applies all active filters (year + region + borough) to make the final filtered dataset.

**Consumed by:** `safest_borough`, `heatmap_totalcrime` and any other plots/table that uses`filtered_df()`

### Complexity Enhancement

In our dashboard, we have implemented a reset button to allow users to easily clear their selected boroughs and crime types. This is an extremely user-friendly feature, as it saves time and prevents users from having to manually deselect each selected option one by one. Without this functionality, users would be required to complete a repetitive and tedious task every time they want to start a new search or adjust their filters.

One of the most important aspects of user experience when designing dashboards and websites is ensuring that users are not forced to complete actions that are time-consuming, frustrating, or unnecessary. A well-designed interface should reduce effort wherever possible and make interactions feel smooth and intuitive. By adding the reset button, we streamline the filtering process and allow users to quickly return to a default state. This small but thoughtful design choice significantly improves usability and creates a more efficient and enjoyable experience overall.

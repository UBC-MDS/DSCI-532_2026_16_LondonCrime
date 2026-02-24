### Updated Job Stories

+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------+-------------------------------------------------------------------------------------------------------------------------+
| Job Story                                                                                                                                                                                                                                                                                                        | Status     | Notes                                                                                                                   |
+==================================================================================================================================================================================================================================================================================================================+============+=========================================================================================================================+
| My family and I are from the United States and we want to visit London for a summer trip. We have two kids under the age of five and we want to make sure our hotel is in a safe and quiet neighborhood. We want to make sure the location of our hotel has the lowest crime rate across all boroughs of London. | ⏳ Pending | Need the box at the top right of the dashboard to show the borough with the lowest crime rate.                          |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------+-------------------------------------------------------------------------------------------------------------------------+
| I have recently moved from Barcelona, Spain to London. I work at home and want to ensure the borough I move into has the lowest crime rate. This would ensure that I could safely stay home, and not worry about any solicitors and intruders, especially at night.                                              | ⏳ Pending | Need the box at the top right of the dashboard to show the borough with the lowest crime rate.                          |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------+-------------------------------------------------------------------------------------------------------------------------+
| I work at a law firm, and our client was robbed of his possessions in Barnet, a borough in London. The defense argues that no crimes have occurred in that borough for the past two years. Using this dashboard, we can quickly validate or disprove this claim.                                                 | ⏳ Pending | Need to make sure the heat map shows each borough and how many crimes have taken place there in the past several years. |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------+-------------------------------------------------------------------------------------------------------------------------+

### Component Inventory

+----------------------+----------------------+-------------------------+------------------+---------------+
| ID                   | Type                 | Shiny widget / renderer | Depends on       | **Job story** |
+======================+======================+=========================+==================+===============+
| `filtered_year`      | Reactive calculation | `@reactive.calc`        | `input_year`     | #1            |
|                      |                      |                         |                  |               |
|                      |                      |                         |                  | #2            |
+----------------------+----------------------+-------------------------+------------------+---------------+
| `filtered_df`        | Reactive calculation | `@reactive.calc`        | `input_year`,    | #3            |
|                      |                      |                         |                  |               |
|                      |                      |                         | `input_region` , |               |
|                      |                      |                         |                  |               |
|                      |                      |                         | `input_borough`  |               |
+----------------------+----------------------+-------------------------+------------------+---------------+
| `filtered_region`    | Reactive calculation | `@reactive.calc`        | `input_region`   | #3            |
+----------------------+----------------------+-------------------------+------------------+---------------+
| `safest_borough`     | Output               | `@render.text`          | `filtered_df`    | #1            |
|                      |                      |                         |                  |               |
|                      |                      |                         |                  | #2            |
+----------------------+----------------------+-------------------------+------------------+---------------+
| `input_borough`      | Input                | `ui.input_text`         | NA               | #1            |
|                      |                      |                         |                  |               |
|                      |                      |                         |                  | #2            |
|                      |                      |                         |                  |               |
|                      |                      |                         |                  | #3            |
+----------------------+----------------------+-------------------------+------------------+---------------+
| `heatmap_totalcrime` | Output               | `@render.plot`          | `filtered_df`    | #3            |
+----------------------+----------------------+-------------------------+------------------+---------------+

### Reactivity Diagram

`@reactive.calc`

``` mermaid
flowchart TD
  Y[/input_year/] --> FY{{filtered_year}}
  R[/input_region/] --> FR{{filtered_region}}
  B[/input_borough/] --> FD{{filtered_df}}
  FY --> FD
  FR --> FD
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
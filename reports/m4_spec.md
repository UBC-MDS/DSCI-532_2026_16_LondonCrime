## Decisions Before Coding Milestone 4

#### 1. Data Access using Parquet and DuckDB

In order to improve the performance of our dashboard, the processed dataset will be stored in Parquet format. Parquet allows an efficient reading of the columns needed for analysis, which will help reduce memory usage and speed up the queries compared to loading the entire CSV files.

With the use of DuckDB, the dashboard will access Parquet dataset through `ibis` interface. DuckDB would act as an embedded analytical database that would help the SQL style queries to be performed and executed directly on the Parquet files without loading the entire dataset into memory.

Through this, the dashboard would filter everything at the database query level which uses reactive calculations. Therefore, when a user changes an input, the query would update and DuckDB would only return the rows that match the selected filters.

The filtered results will be converted to a pandas DataFrame and visualized using the visualization components. This would allow the dashboard to only load necessary data, and improve responsiveness, making the application more suitable for larger datasets.

#### 2. Advanced feature (Component click event interaction)

The dashboard will feature interactions through output components. The bar in the crime category bar chart, for example, would act as a filter, and update the background dataset, which causes all other components of the dashboard to update as well, accordingly.

#### 3. Testing strategy

With the use of **Playwright**, the dashboard behavior will be tested. This will ensure and verify whether filtering and interactions behave correctly and at least three UI behaviors will be tested as well. These tests will act as a user interaction with the dashboard to make sure that inputs are correctly update the visualization and data.

#### 4. Feedback changes

Based on the peer reviewed received from peers, instructor, and TAs, our dashboard will be improved by enhancing or implementing critical or non-critical feedback. Critical items that might include broken functionality or usability concerns will be prioritized and resolved to ensure the dashboard is running properly and provides reliable user experience. Furthermore, other non-critical issues will be addressed if there are not enough critical issues. These issues might include clarify of visualization, and responsiveness of the application.
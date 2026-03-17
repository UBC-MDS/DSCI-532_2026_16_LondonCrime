# Changelog

## [0.4.0] - 2026-03-13

### Added

- AI Assistant tab: natural-language queries over London crime data with filtered plots (e.g. by borough, crime type, year). (#86)
- Interactive crime type breakdown: click crime types in the chart to filter the dashboard; "Clear selection" resets. (#84)
- Lazy loading for the main dashboard to improve initial load time. (#82)
- Test suite for the app (e.g. `tests/test_app.py`). (#83)

### Changed

- Refactored data loading in `app.py` for clarity and reuse.
- Requirements: removed unused packages, added new dependencies; cleaned `requirements.txt` and `requirements_clean.txt`.
- Add click interaction to the crime type breakdown chart to filter the dashboard to those crime types.
- Updated AI chatbot greeting.
- Added test suite for the app.

### Fixed

- Removed redundant panels from AI Assistant tab.

- **Feedback prioritization issue link:** #67

### Known Issues

- AI chatbot can take a very long time to load, even on the first message.

### Release Highlight: Interactive crime type breakdown (click-to-filter)

The crime type breakdown chart is now interactive: users can click one or more crime types in the legend or chart to filter the entire dashboard to those types, then use "Clear selection" to reset. This supports quick drill-down (e.g. compare only "Theft and Handling" and "Violence Against the Person" across the two boroughs) without leaving the main view.

- **Option chosen:** Option D
- **PR:** #84
- **Why this option over the others:** The other options were either too complex or not as useful for the user. Option D was the simplest and most useful for the user.
- **Feature prioritization issue link:** #67

### Collaboration

- **CONTRIBUTING.md:** Updated with M3 retrospective and M4 norms (#72).
- **M3 retrospective:** Documented what worked (e.g. lab-day issue creation and assignment, one major task per member) and what didn’t (merge conflicts from parallel edits to `app.py`, uneven coding vs writing, missed Thursday check-ins, unclear ownership of release/submission, thin PR documentation).
- **M4:** Committed to better PR descriptions and explicit approvals, more frequent PRs to avoid merge conflicts, balanced coding and writing per member, and a Wednesday/Thursday check-in for meetings.

### Reflection

**What the dashboard does well:** The two-borough comparison keeps the focus clear and makes summary cards and plots directly comparable; the sidebar filters (date, crime type, borough) and interactive crime-type breakdown support flexible exploration without overwhelming the user. Lazy loading improves perceived performance on first load.

**Current limitations:** The AI Assistant remains slow to load and is not fully aligned with the dashboard’s two-borough framing, which can be confusing. Some charts still repeat information; making each chart a distinct unit of insight would be a good next step.

**Trade-offs:** Feedback was prioritized to ship the interactive crime-type filter and AI Assistant integration first; full rationale is in the feedback prioritization issue. 

**Most useful:** The AI Assistant lecture and material was very helpful for implementing the AI Assistant tab.

## [0.3.0]

### Added

- Added an AI chatbot tab that filters the data based on user input and implements a selection of plots using the filtered data. The AI chatbot is not set up specifically for borough comparisons, as it is based off of the version 0.2.0 dashboard.

### Changed

- Made the plots into their own tabs inside the main dashboard so that they are easier to view in large format. Chose the stacked bar plot as the default view plot, since it provides a good summary of the two comparison boroughs and their relative amount of crime and crime type breakdown.
- Changed dashboard format to an exactly two borough comparison
- Updated side selector to select exactly two boroughs, with the lowest and highest crime boroughs as the defaults
- Redesigned plots to showcase borough comparisons
- Removed trend line plot and crime type vs month heat map plot, as they did not facilitate easy borough comparison
- Combined summary cards such that each summary card has average crime rate, lowest, and highest crime type. Created three summary cards: one for each comparison borough and one for the city of london at large to use as a baseline.

### Fixed

- Summary cards and plots now handle empty filtered data gracefully, displaying "No Data" instead of errors when filters return no results.
- Fix cards being too small for readability.

### Known Issues

- AI chatbot can take a very long time to load, even on the first message.

### Reflection

The two borough comparison makes the summary cards much more useful, and makes it easier to compare to a baseline (all boroughs). The graphs contain some repeated information, and additional graph design to make each graph its own unit of important information would be a good next step. That the dashboard and the AI chatbot aren't completely aligned (the dashboard is hyperfocused on two borough comparison, while the AI chatbot allows for broader inquiries) may be confusing to some users.

## [0.2.0]

### Added

- Sidebar controls for date range selection, crime type filters, borough multi-select, and a reset button.
- Value boxes for key summary metrics (total crimes, crime rate, most common crime, and lowest crime borough).
- Card layout with placeholder panels for borough trend comparison, crime type distribution, crime-type trend comparison, a borough–month heatmap, and a recent incidents view.

### Changed

- Structured the dashboard layout so that key headline metrics appear above the main visualizations.
- Aligned the planned views more closely with the Milestone 1 proposal.

### Fixed

- Populated the placeholder panels with the data from the dataset.

### Known Issues

- Performance and usability have not yet been tested on the full raw dataset.

### Reflection

Building out the UI skeleton helped clarify how users will move between filters, headline metrics, and detailed views, and surfaced several design decisions (such as placing key numbers above the plots and grouping related charts together). This milestone is a good starting point for the implementation of the dashboard.
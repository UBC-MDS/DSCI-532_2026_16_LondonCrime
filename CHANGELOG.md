# Changelog

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
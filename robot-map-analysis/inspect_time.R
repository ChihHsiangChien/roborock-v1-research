
library(jsonlite)
data <- fromJSON("map_dump.json")

# Check path entity metadata
if (!is.null(data$map$entities)) {
  for (i in seq_along(data$map$entities$type)) {
    if (data$map$entities$type[i] == "path") {
      cat("Path Metadata:\n")
      print(data$map$entities$metaData[i, ])
    }
  }
}

# Search for any time or statistics
print("Searching for 'time' or 'area' in entire JSON structure:")
all_names <- names(unlist(data))
print(all_names[grep("(time|area|statistics)", all_names, ignore.case=TRUE)])

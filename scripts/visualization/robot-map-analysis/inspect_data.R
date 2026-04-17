
library(jsonlite)
data <- fromJSON("map_dump.json")

# Print all attribute classes and their contents
for (i in seq_along(data$attributes$`__class`)) {
  cat("Attribute class:", data$attributes$`__class`[i], "\n")
  print(data$attributes[i, ])
}

# If no CurrentStatisticsStateAttribute, search elsewhere
if (!"CurrentStatisticsStateAttribute" %in% data$attributes$`__class`) {
  print("CurrentStatisticsStateAttribute not found in top-level attributes.")
}

# Check entities for path data
if (!is.null(data$map$entities)) {
  for (i in seq_along(data$map$entities$type)) {
    cat("Entity type:", data$map$entities$type[i], "\n")
    if (data$map$entities$type[i] == "path") {
      cat("Path length:", length(data$map$entities$points[[i]]), "\n")
      # Check if path points have timestamps or other info
      # points is usually a matrix or list of coords [x, y]
      print(head(data$map$entities$points[[i]]))
    }
  }
}

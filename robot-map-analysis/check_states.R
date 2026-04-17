
library(jsonlite)
lines <- readLines("map_dump.json")
first <- fromJSON(lines[1])
last <- fromJSON(lines[length(lines)])

get_battery <- function(attr) {
  if (is.null(attr)) return(NA)
  idx <- which(attr$`__class` == "BatteryStateAttribute")
  if (length(idx) > 0) return(attr$level[idx])
  return(NA)
}

cat("First Battery:", get_battery(first$attributes), "\n")
cat("Last Battery:", get_battery(last$attributes), "\n")
cat("Total Lines:", length(lines), "\n")

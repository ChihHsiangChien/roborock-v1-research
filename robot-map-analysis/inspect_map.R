
library(jsonlite)
data <- fromJSON("map_dump.json")

# Check layers
print("Layers:")
print(data$map$layers$type)

# Check entities
if (!is.null(data$map$entities)) {
  print("Entities:")
  print(data$map$entities$type)
} else {
  print("No entities found in map.")
}

# Check attributes
print("Attributes:")
print(data$attributes$`__class`)

variable "project_id" {
  type        = string
  description = "The project ID. Changing this forces a new project to be created."
}

variable "tables" {
  type        = map(list(string))
  description = "Origin and tables to extract."
}

variable "origins" {
  type        = map(string)
  description = "Origins and origin type."
}
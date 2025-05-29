variable "project_id" {
  type        = string
  description = "The project ID. Changing this forces a new project to be created."
}

variable "bq_sap" {
  type = list(object({
    dataset           = string
    description       = string
    location          = string
    storage_path      = string
    tables            = list(string)
  }))
}

variable "bq_datasets" {
  type = list(object({
    dataset           = string
    description       = string
  }))
}

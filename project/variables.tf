variable "project_name" {
  type        = string
  description = " The display name of the project."
}

variable "project_id" {
  type        = string
  description = "The project ID. Changing this forces a new project to be created."
}

variable "folder_id" {
  type        = string
  description = "The numeric ID of the folder this project should be created under."
}

variable "billing_account" {
  type        = string
  description = "The alphanumeric ID of the billing account this project belongs to."
}

variable "auto_create_network" {
  type        = bool
  default     = false
  description = "Controls whether the 'default' network exists on the project. Defaults to false, where it is not created."
}

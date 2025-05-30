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

## a partir de aqui
variable "project" {
  description = "Nombre del proyecto"
  type        = string
}

variable "subnet_name" {
  description = "The name of the subnetwork."
  type        = string
}

variable "region" {
  description = "The region of the subnetwork."
  type        = string
}

variable "zone" {
  description = "The zone of the provider"
  type        = string
}

variable "vpc_name" {
  description = "The name of the VPC network."
  type        = string
}

variable "location" {
  description = "Location of registry"
  type = string
}

variable "repository_id" {
  description = "Id of repository"
  type = string
}

variable "cleanup_policies_id" {
  description = "Id of cleanup policies"
  type = string
}

# variable "data" {
#   description = "El nombre de la red VPC a buscar."
#   type        = list(object({
#     project_id = string 
#     name = string
#     region = string
#   }))
# }

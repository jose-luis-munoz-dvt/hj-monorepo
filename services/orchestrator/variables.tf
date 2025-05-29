variable "git_commitish" {
  type        = string
  description = "Git commit/tag/branch name at which the repository should be compiled. Must exist in the remote repository."
}

variable "repository" {
  type        = string
  description = "Full dataform repository ID"
}

variable "project_id" {
  type        = string
  description = "The project ID. Changing this forces a new project to be created."
}
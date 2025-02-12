variable "git_commitish" {
  type        = string
  description = "Git commit/tag/branch name at which the repository should be compiled. Must exist in the remote repository."
  default     = "dev"
}

variable "repository" {
  type        = string
  description = "Full dataform repository ID"
  default     = "projects/pj-data-des/locations/europe-west1/repositories/dv-df-pj-data"
}
variable "project_id" {
  type        = string
  description = "The project ID. Changing this forces a new project to be created."
  default     = "pj-data-des"
}

variable "tables" {
  type        = map(list(string))
  description = "Origin and tables to extract."
  default = {
    "SAP" = [
      "AUFM", "EKKO", "KNA1", "KNVV", "LFA1", "LFB1", "LFC1", "LFM1", "LFMC",
      "LIKP", "LIPS", "LIPSPO", "MAKT", "MARA", "T001W", "T005T", "T005U",
      "T006", "T016T", "TPAR", "TVK0T", "TVK9T", "TVKOT", "TVST", "VBAK",
      "VBSK", "VBUK", "VEKP", "VEPVG", "VTTK"
    ]
    "SIMATIC_IT" = ["LogEnergia", "LogEnergiaCircutor"],
    # "CIRCUTOR_PA_PS" = ["devices", "engines", "std_wat_values"]
  }
}

variable "origins" {
  type        = map(string)
  description = "Origins and origin type."
  default = {
    "SAP"        = "SAP"
    "SIMATIC_IT" = "SQL_SERVER"
    # "CIRCUTOR_PA_PS" = "SQL_SERVER"
  }
}

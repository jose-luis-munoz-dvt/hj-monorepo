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
      "AUFM", "EKKO", "KNA1", "KNVV", "LFA1", "LFB1", "LFC1", "LFM1",
      "LIKP", "LIPS", "MAKT", "MARA", "T001W", "T005T", "T005U",
      "T006", "T016T", "TPAR", "TVK0T", "TVK9T", "TVKOT", "TVST", "VBAK",
      "VBSK", "VBUK", "VEKP", "VEPVG", "VTTK", "MSEG", "MKPF", "PLMK",
      "QAMR", "QAMV", "VBRK", "VBRP", "MCHB", "EKBE", "T134T", "T023T",
      "VBAP", "EKPO", "INOB", "AUSP", "QALS", "MBEW", "T179T", "A305",
      "A304", "A978", "A980", "A977", "A979", "KONV", "KONP", "QAVE",
    ]
    "SIMATIC_IT" = ["LogEnergia", "LogEnergiaCircuitor"]
    "GREYCON_VAR" = [
      "VAR_CMI_PRODCTION_DAY", "VAR_CMI_STOPPAGE_DAY", "VAR_CMI_PRODUCTION_GRADE",
      "VAR_CMI_CUSTOMERS", "VAR_CMI_PRODUCT", "VAR_CMI_ITEM", "VAR_CMI_MACHINE", "V_VAR_CMI_DELIVERY", "V_VAR_CMI_STK"
    ]
    "VOLUPACK_VAR"           = ["V_CMI_VAR_SUPPLIERS", "V_CMI_VAR_MVT_ITEM", "V_CMI_VAR_ITEM_PURCHASE", "VAR_CMI_VAR_INVOICE", "V_CMI_VAR_ITEM", "V_CMI_VAR_CUSTOMER"]
    "CIRCUTOR_PA_PS"         = ["Devices", "Engines", "std_wat_values", "Variables"]
    "CIRCUTOR_VAR"           = ["Devices", "Engines", "std_wat_values", "Variables"]
    "VEOLIA"                 = ["DATOS_VAPOR"]
    "NEOELECTRA_SARRIA"      = ["CONFIG_FILE"]
    "NEOELECTRA_FRANCE"      = ["CONFIG_FILE"]
    "HINOJOSA_AEV_SEH"       = ["CONFIG_FILE"]
    "HINOJOSA_AEV_LOGISTICA" = ["CONFIG_FILE"]
    "HINOJOSA_RECLAMACIONES" = ["CONFIG_FILE"]
  }
}

variable "origins" {
  type        = map(string)
  description = "Origins and origin type."
  default = {
    "SAP"                    = "SAP"
    "SIMATIC_IT"             = "SQL_SERVER"
    "CIRCUTOR_PA_PS"         = "SQL_SERVER"
    "CIRCUTOR_VAR"           = "SQL_SERVER"
    "GREYCON_VAR"            = "SQL_SERVER"
    "VOLUPACK_VAR"           = "ORACLE"
    "VEOLIA"                 = "GOOGLE_DRIVE"
    "NEOELECTRA_SARRIA"      = "SHAREPOINT_FILES"
    "NEOELECTRA_FRANCE"      = "SHAREPOINT_FILES"
    "HINOJOSA_AEV_SEH"       = "SHAREPOINT_FILES"
    "HINOJOSA_AEV_LOGISTICA" = "SHAREPOINT_FILES"
    "HINOJOSA_RECLAMACIONES" = "SHAREPOINT_LISTS"
  }
}

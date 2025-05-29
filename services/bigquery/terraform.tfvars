project_id = "pj-data-des"
bq_sap = [
    {
      dataset      = "origen_sap"
      description  = "Tablas extraidas de SAP"
      location     = "EU"
      storage_path = "SAP/SAP"
      tables = [
        "AUFM", "EKKO", "KNA1", "KNVV", "LFA1", "LFB1", "LFC1", "LFM1",
        "LIKP", "LIPS", "MAKT", "MARA", "T001W", "T005T", "T005U",
        "T006", "T016T", "TPAR", "TVK0T", "TVK9T", "TVKOT", "TVST", "VBAK",
        "VBSK", "VBUK", "VEKP", "VEPVG", "VTTK", "MSEG", "MKPF", "PLMK",
        "QAMR", "QAMV", "VBRK", "VBRP", "MCHB", "EKBE", "T134T", "T023T",
        "VBAP", "EKPO", "INOB", "QALS", "MBEW", "T179T", "A305", # "AUSP",
        "A304", "A978", "A980", "A977", "A979", "KONV", "KONP", "QAVE",
      ]
    }
  ]

bq_datasets = [
  {
    dataset      = "raw_data"
    description  = "Raw data tables from data sources"
  },
  {
    dataset      = "d_hechos"
    description  = "Tablas de hechos "
  },
  {
    dataset      = "d_staging"
    description  = "Tablas staging"
  },
  {
    dataset      = "origen_simatic"
    description  = "Tablas extraidas de Simatic SQL Server"
  },
  {
    dataset      = "origen_circutor"
    description  = "Tablas extraidas de Circutor SQL Server"
  },
  {
    dataset      = "origen_drive"
    description  = "Tablas extraidas de Google Drive"
  },
  {
    dataset      = "origen_neolectra"
    description  = "Tablas extraidas del sharepoint de neolectra"
  },
  {
    dataset      = "origen_sharepoint"
    description  = "Tablas extraidas de sharepoint"
  },
  {
    dataset      = "d_dimensiones"
    description  = "Tablas de dimensiones"
  }
]

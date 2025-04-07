import os
from google.cloud import secretmanager

############### CONFIG ###############

ROWS_PER_BATCH = int(os.getenv("ROWS_PER_BATCH", 25000))
CHUNK_SIZE     = int(os.getenv("CHUNK_SIZE", 20))
LOAD_MODE = os.environ.get("LOAD_MODE")
INCREMENTAL_TIMESTAMP_SOURCE =  os.environ.get("INCREMENTAL_TIMESTAMP_SOURCE",None)
INCREMENTAL_FIELD = os.environ.get("INCREMENTAL_FIELD",None)
ENVIROMENT = os.environ.get("ENVIROMENT","des")

GCS_BUCKET_ID  = f"gcs-pj-data-{ENVIROMENT}-data-extraction"
GCP_PROJECT_ID = f"pj-data-{ENVIROMENT}"

########### SECRET MANAGER ###########

secrets_client = secretmanager.SecretManagerServiceClient()

def access_secret(secret_id, version_id="latest"):
    name = f"projects/{GCP_PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
    response = secrets_client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')

################ SAP #################

SAP_HOST    = "10.200.32.210"
SAP_PORT    = 30044
SAP_USER    = access_secret('DWH_SAP_USER')
SAP_PWD     = access_secret('DWH_SAP_PWD')
SAP_DB_NAME = "HEP"

############# SHAREPOINT #############

SHAREPOINT_FILE_ORIGINS = {
    # "HINOJOSA": {
    #     "TENANT_ID":     "f95c33c5-2761-4ebd-a34b-07b48878c723",
    #     "CLIENT_ID":     "b34ee42c-b63d-482b-8bc5-8abad40178ce",
    #     "CLIENT_SECRET": access_secret('DWH_AZURE_CLIENT_SECRET'),
    #     "AZ_USERNAME":   access_secret('DWH_AZURE_USER'),
    #     "AZ_PASS":       access_secret('DWH_AZURE_PWD'),
    #     "SITE_ID":       "hinojosagroup.sharepoint.com,ff26b08f-de4a-455f-9561-ee3e1446a3a3,ebf650e1-744d-4b75-802a-fbd07bc1e2ed",
    #     "DRIVE_ID":      "b!j7Am_0reX0WVYe4-FEajo-FQ9utNdHVLgCr70HvB4u34ZpJvqZmJTbmzkbX3CRtN",
    #     "FILE_PATH":     "IT-07 GESTIÓN DE APLICACIONES/02 - BI/Prueba_Datos/Produccion/",
    #     "FILE_NAMES":    {
    #         "Maquinas.xlsx":[]
    #     }
    # },
    "HINOJOSA_AEV_SEH": {
        "TENANT_ID":     "f95c33c5-2761-4ebd-a34b-07b48878c723",
        "CLIENT_ID":     "b34ee42c-b63d-482b-8bc5-8abad40178ce",
        "CLIENT_SECRET": access_secret('DWH_AZURE_CLIENT_SECRET'),
        "AZ_USERNAME":   access_secret('DWH_AZURE_USER'),
        "AZ_PASS":       access_secret('DWH_AZURE_PWD'),
        "SITE_ID":       "hinojosagroup.sharepoint.com,ff26b08f-de4a-455f-9561-ee3e1446a3a3,35bd9e52-a991-44d3-8c96-f68dd77008e8",
        "DRIVE_ID":      "b!j7Am_0reX0WVYe4-FEajo1KevTWRqdNEjJb2jddwCOgmYhyw_U93TpN-ATxdqGiT",
        "FILE_PATH":     "04. Energie/",
        "FILE_NAMES":    {
            "Relevés Chaudière Biogaz.xlsx": ["BIOGAZ"]
        }
    },
    "HINOJOSA_AEV_LOGISTICA": {
        "TENANT_ID":     "f95c33c5-2761-4ebd-a34b-07b48878c723",
        "CLIENT_ID":     "b34ee42c-b63d-482b-8bc5-8abad40178ce",
        "CLIENT_SECRET": access_secret('DWH_AZURE_CLIENT_SECRET'),
        "AZ_USERNAME":   access_secret('DWH_AZURE_USER'),
        "AZ_PASS":       access_secret('DWH_AZURE_PWD'),
        "SITE_ID":       "hinojosagroup.sharepoint.com,ff26b08f-de4a-455f-9561-ee3e1446a3a3,abd2fabe-5150-4684-9c81-6226cc41e529",
        "DRIVE_ID":      "b!j7Am_0reX0WVYe4-FEajo7760qtQUYRGnIFiJsxB5SmG1zpJhqyVR67RQK1liaBK",
        "FILE_PATH":     "VLOG FICHIER MOUVEMENTS/",
        "FILE_NAMES":    {
            "VLOG E001 BILAN LOGISTIQUE.*\\.xlsx": []
        }
    },
    "NEOELECTRA_SARRIA": {
        "TENANT_ID":     "06dda825-540e-4751-91f8-62bd70bd97e5",
        "CLIENT_ID":     "3669644c-b7fe-4a06-98a8-71ecc7bb182f",
        "CLIENT_SECRET": access_secret('DWH_NEOELECTRA_CLIENT_SECRET'),
        "AZ_USERNAME":   access_secret('DWH_NEOELECTRA_USER'),
        "AZ_PASS":       access_secret('DWH_NEOELECTRA_PWD'),
        "SITE_ID":       "neoelectra.sharepoint.com,b3464bda-31a7-48b8-9772-f7afbe11eaa6,6ddbcfe2-dbd5-4485-ac43-20389a4afd34",
        "DRIVE_ID":      "b!2ktGs6cxuEiXcvevvhHqpuLP223V24VErEMgOJpK_TQ_EmBrxPBzRJvSJx7HOMqr",
        "FILE_PATH":     "GN-FRANCE/SARRIA/",
        "FILE_NAMES":    {
            "CPT V2.xlsx": ["índice Contador "]
        }
    },
    "NEOELECTRA_FRANCE": {
        "TENANT_ID":     "06dda825-540e-4751-91f8-62bd70bd97e5",
        "CLIENT_ID":     "3669644c-b7fe-4a06-98a8-71ecc7bb182f",
        "CLIENT_SECRET": access_secret('DWH_NEOELECTRA_CLIENT_SECRET'),
        "AZ_USERNAME":   access_secret('DWH_NEOELECTRA_USER'),
        "AZ_PASS":       access_secret('DWH_NEOELECTRA_PWD'),
        "SITE_ID":       "neoelectra.sharepoint.com,b3464bda-31a7-48b8-9772-f7afbe11eaa6,6ddbcfe2-dbd5-4485-ac43-20389a4afd34",
        "DRIVE_ID":      "b!2ktGs6cxuEiXcvevvhHqpuLP223V24VErEMgOJpK_TQ_EmBrxPBzRJvSJx7HOMqr",
        "FILE_PATH":     "GN-FRANCE/FRANCE/COMPTEURS ENERGIES/",
        "FILE_NAMES":    {
            "CPT ALLARD V4.xlsm": ["SAISIES", "Relevé_Conso"]
        }
    }
}

SHAREPOINT_LIST_ORIGINS = {
    "HINOJOSA_RECLAMACIONES": {
        "TENANT_ID":     "f95c33c5-2761-4ebd-a34b-07b48878c723",
        "CLIENT_ID":     "b34ee42c-b63d-482b-8bc5-8abad40178ce",
        "CLIENT_SECRET": access_secret('DWH_AZURE_CLIENT_SECRET'),
        "AZ_USERNAME":   access_secret('DWH_AZURE_USER'),
        "AZ_PASS":       access_secret('DWH_AZURE_PWD'),
        "SITE_ID":       "hinojosagroup.sharepoint.com,6acd5dae-fe66-4a67-b445-4e8806d5e008,a0a16e3c-b585-4c8a-93b5-325f82dc9e64",
        "LISTS":         ["Reclamaciones", "Planta", "Papelera", "Tipo de incidencia", "Motivo", "Abono", "Origen", "Gravedad", "Departamento", "Bobinadora"]
    },
}

############# SIMATIC IT #############

SQL_SERVER_ORIGINS = {
    "SIMATIC_IT": {
        "host": "192.168.75.53",
        "user": access_secret('DWH_SIMATIC_USER'),
        "pwd": access_secret('DWH_SIMATIC_PWD'),
        "db_name": "MavalBI",
    },
    "CIRCUTOR_PA_PS": {
        "instance_name": "SQLEXPRESS",
        "host": "192.168.75.21",
        "user": access_secret('DWH_CIRCUTOR_USER'),
        "pwd": access_secret('DWH_CIRCUTOR_PWD'),
        "db_name": "SQLDataExportSQL",
        "schema": "SQLDataExport"
    },
    "CIRCUTOR_VAR": {
        "instance_name": "SQLEXPRESS",
        "host": "10.72.250.11",
        "user": access_secret('DWH_CIRCUTOR_VAR_USER'),
        "pwd": access_secret('DWH_CIRCUTOR_VAR_PWD'),
        "db_name": "SQLDataExportSQL",
        "schema": "SQLDataExport"
    },
    "GREYCON_VAR": {
        "host": "10.72.250.102",
        "user": access_secret('DWH_GREYCON_USER'),
        "pwd": access_secret('DWH_GREYCON_PWD'),
        "db_name": "GreyconMill",
    }
}

ORACLE_ORIGINS = {
    "VOLUPACK_VAR": {
        "host": "10.93.4.22",
        "port": 1521,
        "user": access_secret('DWH_VOLUPACK_USER'),
        "pwd": access_secret('DWH_VOLUPACK_PWD'),
        "db_name": "ALLARD",
        "schema": "ATLAS",
    }
}

############ GOOGLE DRIVE ############

GOOGLE_DRIVE_DOCS = {
    "VEOLIA": {
        "DATOS_VAPOR": {
            "doc_id": "2PACX-1vRHCV8aIdizjRq_dDFz59NEj4sr8fWpCSOh__pwf1TIYptTHvNeeUMc4-WZCj-ydRvg4whYuJcJXdlS",
            "sheets": [("PALQ_DATOS_BIOGAS", "1772227349"), ("PSAR_DATOS_BIOGAS", "1622470711"), ("PALQ_DATOS_VAPOR", "52421144"), ("PSAR_DATOS_VAPOR", "462217089"), ("PSAR_DATOS_VEOLIA", "1670830991")]
        }
    }
}

resource "google_workflows_workflow" "wf_orchestrator" {
  name            = "wf_orchestrator"
  region          = "europe-southwest1"
  description     = "Orquestación de extracción de tablas con Cloud Run y ejecucion de Dataform"
  service_account = google_service_account.wf_service_account.id
  user_env_vars = {
    gitCommitish = var.git_commitish
    location = "europe-southwest1"
    repository = var.repository
  }
  source_contents = <<-EOF
main:
    params: [input]
    steps:
    - init:
        assign:
        - project_id: $${sys.get_env("GOOGLE_CLOUD_PROJECT_ID")}
        - location: $${sys.get_env("location")}
        - cloud_run_job_names_list: []
        - repository: $${sys.get_env("repository")}
    - logInit:
        call: sys.log
        args:
            severity: "INFO"
            text: "Inicio carga."
    - cloudRunJobList:
        call: googleapis.run.v2.projects.locations.jobs.list
        args:
            parent: $${"projects/" + project_id + "/locations/" + location}
            pageSize: 100
        result: cloud_run_jobs_list
    - loopCloudRunJobs:
        for:
            value: cloud_run_job
            in: $${cloud_run_jobs_list.jobs}
            steps:
                - appendName:
                    assign:
                        - cloud_run_job_names_list: $${list.concat(cloud_run_job_names_list, cloud_run_job.name)}
    
    - parallelCloudRunJobRun:
        parallel:
            for:
                value: cloud_run_job_name
                in: $${cloud_run_job_names_list}
                steps:
                    - cloudRunJobRun:
                        call: googleapis.run.v2.projects.locations.jobs.run
                        args:
                            name: $${cloud_run_job_name}
                            connector_params:
                                timeout: 21600
    - createCompilationResult:
        call: http.post
        args:
            url: $${"https://dataform.googleapis.com/v1beta1/" + repository + "/compilationResults"}
            auth:
                type: OAuth2
            body:
                gitCommitish: $${sys.get_env("gitCommitish")}
                # codeCompilationConfig:
                #     defaultDatabase: $${sys.get_env("defaultDatabase")}
                #     schemaSuffix: $${sys.get_env("schemaSuffix")}
        result: compilationResult
    - createDataformWorkflowInvocation:
        try:
            call: http.post
            args:
                url: $${"https://dataform.googleapis.com/v1beta1/" + repository + "/workflowInvocations"}
                auth:
                    type: OAuth2
                body:
                    compilationResult: $${compilationResult.body.name}
                    invocationConfig:
                        includedTags: 
                        - pj-data
            result: workflowInvocation
        retry: $${http.default_retry}
    - waitForDataformWorkflowInvocationCompletion:
        steps:
            - checkStatus:
                call: http.get
                args:
                    url: $${"https://dataform.googleapis.com/v1beta1/" + workflowInvocation.body.name}
                    auth:
                        type: OAuth2
                result: workflowInvocationStatus
            - checkIfDone:
                switch:
                    - condition: $${workflowInvocationStatus.body.state == "SUCCEEDED"}
                      next: logEnd
                    - condition: $${workflowInvocationStatus.body.state == "RUNNING"}
                      next: wait
                    - condition: $${not(workflowInvocationStatus.body.state in ["SUCCEEDED", "RUNNING"])}
                      raise: "Error en la ejecución de Dataform"
            - wait:
                call: sys.sleep
                args:
                    seconds: 30
                next: checkStatus

    - logEnd:
        call: sys.log
        args:
            severity: "INFO"
            text: "Finalizada carga."

    - complete:
        return: "Success"
EOF
}
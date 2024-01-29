# Pipeline watcher

This project is used to connect to a "pipeline monitor" that contains informations about all running pipelines in GitLab and display info about status of those pipelines.

## Configuration

The pipeline monitor url must be passed as environment variabile:
`PIPELINE_MONITOR_URL`

For example:

```bash
export PIPELINE_MONITOR_URL="https://pipeline-monitor.example.org"
```
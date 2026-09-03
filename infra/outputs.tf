output "app_url" {
  description = "URL where the BMI app is reachable"
  value       = "http://localhost:${docker_container.app.ports[0].external}"
}

output "app_container_name" {
  description = "Name of the running app container"
  value       = docker_container.app.name
}

output "db_container_name" {
  description = "Name of the running database container"
  value       = docker_container.postgres.name
}

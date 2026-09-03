resource "docker_image" "app" {
  name = "bmi-app:latest"

  build {
    context    = "${path.module}/../app"
    dockerfile = "Dockerfile"
  }
}

resource "docker_container" "app" {
  name  = "bmi-app"
  image = docker_image.app.image_id

  ports {
    internal = 8080
    external = 8080
  }

  env = [
    "DATABASE_HOST=bmi-db",
    "DATABASE_PORT=5432",
  ]

  networks_advanced {
    name = docker_network.app_net.name
  }

  restart = "unless-stopped"

  depends_on = [docker_container.postgres]
}

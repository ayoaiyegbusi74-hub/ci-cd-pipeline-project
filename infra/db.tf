resource "docker_image" "postgres" {
  name = "postgres:16-alpine"
}

resource "docker_container" "postgres" {
  name  = "bmi-db"
  image = docker_image.postgres.image_id

  env = [
    "POSTGRES_USER=bmi_app",
    "POSTGRES_PASSWORD=${var.db_password}",
    "POSTGRES_DB=bmi_db",
  ]

  networks_advanced {
    name = docker_network.app_net.name
  }

  volumes {
    volume_name    = docker_volume.postgres_data.name
    container_path = "/var/lib/postgresql/data"
  }

  restart = "unless-stopped"
}

resource "docker_volume" "postgres_data" {
  name = "bmi-postgres-data"
}

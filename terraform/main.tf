resource "kubernetes_deployment_v1" "station" {
  metadata {
    name = var.app_name

    labels = {
      app = var.app_name
    }
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        app = var.app_name
      }
    }

    template {
      metadata {
        labels = {
          app = var.app_name
        }
      }

      spec {
        image_pull_secrets {
          name = "ghcr-secret"
        }

        container {
          name  = var.app_name
          image = var.app_image

          port {
            container_port = var.container_port
          }

          env {
            name  = "MYSQL_HOST"
            value = var.mysql_host
          }

          env {
            name  = "MYSQL_PORT"
            value = "3306"
          }

          env {
            name  = "MYSQL_DATABASE"
            value = var.mysql_database
          }

          env {
            name = "MYSQL_USER"

            value_from {
              secret_key_ref {
                name = "station-mysql-secret"
                key  = "MYSQL_USER"
              }
            }
          }

          env {
            name = "MYSQL_PASSWORD"

            value_from {
              secret_key_ref {
                name = "station-mysql-secret"
                key  = "MYSQL_PASSWORD"
              }
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service_v1" "station" {
  metadata {
    name = var.app_name

    labels = {
      app = var.app_name
    }
  }

  spec {
    type = "NodePort"

    selector = {
      app = var.app_name
    }

    port {
      port        = 5000
      target_port = var.container_port
      node_port   = var.node_port
    }
  }
}

output "app_name" {
  description = "Nama Deployment Station"
  value       = kubernetes_deployment_v1.station.metadata[0].name
}

output "service_node_port" {
  description = "Port akses aplikasi"
  value       = kubernetes_service_v1.station.spec[0].port[0].node_port
}

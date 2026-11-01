variable "app_name" {
  type        = string
  description = "name applications Station"
  default     = "station-app"
}

variable "app_image" {
  type        = string
  description = "Image applications di GHCR"
}

variable "replicas" {
  type        = number
  description = "jumlah replika applications"
  default     = 1
}

variable "container_port" {
  type        = number
  description = "port applications Flask"
  default     = 5000
}

variable "node_port" {
  type        = number
  description = "port akses dari luar cluster"
  default     = 30080
}

variable "mysql_host" {
  type        = string
  description = "alamat Host MySql di docker"
  default     = "172.18.0.1"
}

variable "mysql_database" {
  type        = string
  description = "nama database Station"
  default     = "ecommerce_db"
}

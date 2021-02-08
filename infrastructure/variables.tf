variable "account_name" {
  default = "memsb"
}

variable "github_org" {
  default = "memsb"
}

variable "github_token" {
}

variable "stack" {
	default = "scrapemasterofmalt"
}

variable "project" {
	default = "scrape_masterofmalt"
}

variable "app" {
	default = "scan_mom_new_stock"
}

variable "docker_build_image" {
  default = "ubuntu"
}

variable "code_bucket" {
  default = "memsb-lambda-source"
}

.PHONY: plan

init:
	@echo "initialize remote state file"
	rm -rf .terraform/modules/ && \
	terraform init -reconfigure -no-color

validate: init
	@echo "running terraform validate"
	terraform validate -no-color

plan: validate
	@echo "running terraform plan"
	terraform plan -no-color

apply: plan
	@echo "running terraform apply"
	terraform apply -auto-approve -no-color

plan-destroy: validate
	@echo "running terraform plan -destroy"
	terraform plan -destroy -no-color

destroy: init
	@echo "running terraform destroy"
	terraform destroy -force -no-color

module "vpc" {
  source = "./vpc"
}
module "ec2" {
  source = "./web"
  sn=module.vpc.public_sn
  sg = module.vpc.sg
}
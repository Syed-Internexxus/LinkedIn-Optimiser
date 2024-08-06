import * as common from "@nestjs/common";
import * as swagger from "@nestjs/swagger";
import * as nestAccessControl from "nest-access-control";
import { ProfileOptimizationService } from "./profileOptimization.service";
import { ProfileOptimizationControllerBase } from "./base/profileOptimization.controller.base";

@swagger.ApiTags("profileOptimizations")
@common.Controller("profileOptimizations")
export class ProfileOptimizationController extends ProfileOptimizationControllerBase {
  constructor(
    protected readonly service: ProfileOptimizationService,
    @nestAccessControl.InjectRolesBuilder()
    protected readonly rolesBuilder: nestAccessControl.RolesBuilder
  ) {
    super(service, rolesBuilder);
  }
}

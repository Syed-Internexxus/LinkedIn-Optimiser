import { Module, forwardRef } from "@nestjs/common";
import { AuthModule } from "../auth/auth.module";
import { ProfileOptimizationModuleBase } from "./base/profileOptimization.module.base";
import { ProfileOptimizationService } from "./profileOptimization.service";
import { ProfileOptimizationController } from "./profileOptimization.controller";
import { ProfileOptimizationResolver } from "./profileOptimization.resolver";

@Module({
  imports: [ProfileOptimizationModuleBase, forwardRef(() => AuthModule)],
  controllers: [ProfileOptimizationController],
  providers: [ProfileOptimizationService, ProfileOptimizationResolver],
  exports: [ProfileOptimizationService],
})
export class ProfileOptimizationModule {}

import { Module, forwardRef } from "@nestjs/common";
import { AuthModule } from "../auth/auth.module";
import { AppUserModuleBase } from "./base/appUser.module.base";
import { AppUserService } from "./appUser.service";
import { AppUserController } from "./appUser.controller";
import { AppUserResolver } from "./appUser.resolver";

@Module({
  imports: [AppUserModuleBase, forwardRef(() => AuthModule)],
  controllers: [AppUserController],
  providers: [AppUserService, AppUserResolver],
  exports: [AppUserService],
})
export class AppUserModule {}

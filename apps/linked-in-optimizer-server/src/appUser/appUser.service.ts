import { Injectable } from "@nestjs/common";
import { PrismaService } from "../prisma/prisma.service";
import { AppUserServiceBase } from "./base/appUser.service.base";

@Injectable()
export class AppUserService extends AppUserServiceBase {
  constructor(protected readonly prisma: PrismaService) {
    super(prisma);
  }
}

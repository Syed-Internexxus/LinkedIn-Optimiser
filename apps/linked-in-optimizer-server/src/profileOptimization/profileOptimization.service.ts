import { Injectable } from "@nestjs/common";
import { PrismaService } from "../prisma/prisma.service";
import { ProfileOptimizationServiceBase } from "./base/profileOptimization.service.base";

@Injectable()
export class ProfileOptimizationService extends ProfileOptimizationServiceBase {
  constructor(protected readonly prisma: PrismaService) {
    super(prisma);
  }
}

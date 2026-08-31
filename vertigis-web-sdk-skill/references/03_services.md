# VertiGIS Studio Web SDK: Custom Services

## Overview
Services in VertiGIS Studio Web are application-level singletons that manage core business logic, background processing, shared state, and integrations. Unlike components, services do not render DOM elements.

---

## 1. Creating a Custom Service

Extend `ServiceBase` from `@vertigis/web/services`:

```typescript
// src/services/VehicleTrackingService.ts
import { ServiceBase } from "@vertigis/web/services";
import { inject } from "@vertigis/web/services";
import { MapModel } from "@vertigis/web/mapping";

export interface VehicleLocation {
    id: string;
    latitude: number;
    longitude: number;
    speed: number;
}

export default class VehicleTrackingService extends ServiceBase {
    private _pollingIntervalId: any;
    private _vehicles: Map<string, VehicleLocation> = new Map();

    // Lifecycle: initialize the service
    protected async _onInitialize(): Promise<void> {
        await super._onInitialize();
        console.log("VehicleTrackingService initialized.");
    }

    // Start background task
    public startTracking(intervalMs: number = 5000): void {
        if (this._pollingIntervalId) return;

        this._pollingIntervalId = setInterval(async () => {
            await this._fetchVehicleLocations();
        }, intervalMs);
    }

    // Stop background task
    public stopTracking(): void {
        if (this._pollingIntervalId) {
            clearInterval(this._pollingIntervalId);
            this._pollingIntervalId = null;
        }
    }

    private async _fetchVehicleLocations(): Promise<void> {
        try {
            const response = await fetch("https://api.example.com/vehicles");
            const data: VehicleLocation[] = await response.json();
            data.forEach((v) => this._vehicles.set(v.id, v));

            // Broadcast updates via command or event
            this.messages.commands.map.drawGraphic.execute({
                geometry: {
                    type: "point",
                    x: data[0]?.longitude,
                    y: data[0]?.latitude,
                    spatialReference: { wkid: 4326 }
                },
                symbol: {
                    type: "simple-marker",
                    color: "blue"
                }
            });
        } catch (error) {
            console.error("Failed to fetch vehicle locations", error);
        }
    }

    public getVehicle(id: string): VehicleLocation | undefined {
        return this._vehicles.get(id);
    }

    protected async _onDestroy(): Promise<void> {
        this.stopTracking();
        await super._onDestroy();
    }
}
```

---

## 2. Registering the Service

Register the service inside `src/index.ts`:

```typescript
// src/index.ts
import { LibraryRegistry } from "@vertigis/web/config";
import VehicleTrackingService from "./services/VehicleTrackingService";

export default function (registry: LibraryRegistry): void {
    registry.registerService({
        id: "vehicle-tracking-service",
        getService: (config) => new VehicleTrackingService(config),
    });

    // Expose service capabilities via commands
    registry.registerCommandHandler({
        name: "custom.start-vehicle-tracking",
        execute: async (args, context) => {
            const service = context.services.get("vehicle-tracking-service") as VehicleTrackingService;
            service?.startTracking(args?.interval);
        },
    });

    registry.registerCommandHandler({
        name: "custom.stop-vehicle-tracking",
        execute: async (args, context) => {
            const service = context.services.get("vehicle-tracking-service") as VehicleTrackingService;
            service?.stopTracking();
        },
    });
}
```

---

## 3. Injecting Services into Components & Other Services

```typescript
import { ComponentModelBase } from "@vertigis/web/models";
import { inject } from "@vertigis/web/services";
import VehicleTrackingService from "../../services/VehicleTrackingService";

export class DashboardWidgetModel extends ComponentModelBase {
    @inject("vehicle-tracking-service")
    vehicleService: VehicleTrackingService | undefined;

    public onStartClick(): void {
        this.vehicleService?.startTracking();
    }
}
```

import { useState } from "react";
import { CelestialBodyCloseApproachData } from "@/types/asteroid";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Calendar, Gauge, MapPin, Star } from "lucide-react";
import { cn } from "@/helpers/utils";
import { ImpactSimulationCard } from "./ImpactSimulationCard";

interface AsteroidDetailsProps {
  asteroid: CelestialBodyCloseApproachData | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onToggleFavorite: (designation: string) => void;
}

// Função para calcular nível de ameaça baseado na distância
const getThreatLevel = (
  distanceAu: string
): "safe" | "low" | "medium" | "high" | "critical" => {
  const distance = parseFloat(distanceAu);
  if (distance < 0.01) return "critical";
  if (distance < 0.05) return "high";
  if (distance < 0.1) return "medium";
  if (distance < 0.5) return "low";
  return "safe";
};

const threatColors = {
  safe: "bg-success/20 text-success",
  low: "bg-primary/20 text-primary",
  medium: "bg-warning/20 text-warning",
  high: "bg-destructive/20 text-destructive",
  critical: "bg-destructive text-destructive-foreground",
};

const threatLabels = {
  safe: "Seguro",
  low: "Baixo",
  medium: "Médio",
  high: "Alto",
  critical: "Crítico",
};

export const AsteroidDetails = ({
  asteroid,
  open,
  onOpenChange,
  onToggleFavorite,
}: AsteroidDetailsProps) => {
  const [simulationOpen, setSimulationOpen] = useState(false);

  if (!asteroid) return null;

  const threatLevel = getThreatLevel(asteroid.distance_au);

  return (
    <>
      <Dialog open={open} onOpenChange={onOpenChange}>
        <DialogContent className="glass-card border-primary/30 max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <div className="flex items-start justify-between">
              <div>
                <DialogTitle className="text-2xl font-bold gradient-text">
                  {asteroid.designation}
                </DialogTitle>
                <DialogDescription className="mt-2">
                  Designação: {asteroid.designation}
                </DialogDescription>
              </div>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => onToggleFavorite(asteroid.designation)}
                className="transition-colors"
              >
                <Star className="h-6 w-6" />
              </Button>
            </div>
          </DialogHeader>

          <div className="space-y-6 mt-6">
            <div className="flex items-center gap-2">
              <Badge
                className={cn(
                  "font-medium text-sm px-3 py-1",
                  threatColors[threatLevel]
                )}
              >
                Ameaça: {threatLabels[threatLevel]}
              </Badge>
            </div>

            <Separator className="bg-border/50" />

            <div className="grid grid-cols-2 gap-6">
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Gauge className="h-4 w-4 text-primary" />
                  <span className="text-sm">Velocidade</span>
                </div>
                <p className="text-2xl font-bold">
                  {asteroid.velocity_kms} km/s
                </p>
              </div>

              <div className="space-y-2">
                <div className="flex items-center gap-2 text-muted-foreground">
                  <MapPin className="h-4 w-4 text-primary" />
                  <span className="text-sm">Distância Atual</span>
                </div>
                <p className="text-2xl font-bold">{asteroid.distance_au} AU</p>
              </div>
            </div>

            <Separator className="bg-border/50" />

            <div className="space-y-4">
              <div className="flex items-center gap-2 text-muted-foreground">
                <Calendar className="h-4 w-4 text-primary" />
                <span className="text-sm font-semibold">Cronologia</span>
              </div>
              <div className="space-y-3 ml-6">
                <div>
                  <p className="text-sm text-muted-foreground">
                    Próxima Aproximação à Terra
                  </p>
                  <p className="font-semibold text-warning">
                    {new Date(asteroid.close_approach_date).toLocaleDateString(
                      "pt-BR",
                      {
                        day: "numeric",
                        month: "long",
                        year: "numeric",
                      }
                    )}
                  </p>
                </div>
              </div>
            </div>

            <div className="flex gap-3 pt-4">
              <Button
                className="flex-1 bg-primary hover:bg-primary/90 text-primary-foreground"
                onClick={() => setSimulationOpen(true)}
              >
                Impact Simulation
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      {/* Impact Simulation Card */}
      <ImpactSimulationCard
        asteroid={asteroid}
        open={simulationOpen}
        onOpenChange={setSimulationOpen}
      />
    </>
  );
};

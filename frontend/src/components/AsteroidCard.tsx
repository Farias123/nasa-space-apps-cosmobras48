import { CelestialBodyCloseApproachData } from "@/types/asteroid";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Star, Info, Rocket, AlertTriangle } from "lucide-react";
import { cn } from "@/helpers/utils";

interface AsteroidCardProps {
  asteroid: CelestialBodyCloseApproachData;
  onToggleFavorite: (designation: string) => void;
  onViewDetails: (asteroid: CelestialBodyCloseApproachData) => void;
}

// Function to calculate threat level based on distance
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
  safe: "bg-success/20 text-success border-success/50",
  low: "bg-primary/20 text-primary border-primary/50",
  medium: "bg-warning/20 text-warning border-warning/50",
  high: "bg-destructive/20 text-destructive border-destructive/50",
  critical: "bg-destructive text-destructive-foreground border-destructive",
};

const threatLabels = {
  safe: "Safe",
  low: "Low",
  medium: "Medium",
  high: "High",
  critical: "Critical",
};

export const AsteroidCard = ({
  asteroid,
  onToggleFavorite,
  onViewDetails,
}: AsteroidCardProps) => {
  const threatLevel = getThreatLevel(asteroid.distance_au);
  const showWarning = threatLevel === "high" || threatLevel === "critical";

  return (
    <Card className="glass-card transition-all duration-300 hover:scale-[1.02] hover:shadow-lg hover:shadow-primary/20 group">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <CardTitle className="text-xl font-bold flex items-center gap-2">
              {asteroid.designation}
              {showWarning && (
                <AlertTriangle className="h-5 w-5 text-destructive animate-pulse" />
              )}
            </CardTitle>
            <CardDescription className="text-muted-foreground mt-1">
              Designation: {asteroid.designation}
            </CardDescription>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => onToggleFavorite(asteroid.designation)}
            className="transition-colors"
          >
            <Star className="h-5 w-5" />
          </Button>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div className="space-y-1">
            <p className="text-muted-foreground">Velocity</p>
            <p className="font-semibold text-foreground">
              {asteroid.velocity_kms} km/s
            </p>
          </div>
          <div className="space-y-1">
            <p className="text-muted-foreground">Distance</p>
            <p className="font-semibold text-foreground">
              {asteroid.distance_au} AU
            </p>
          </div>
          <div className="space-y-1 col-span-2">
            <p className="text-muted-foreground">Next Approach</p>
            <p className="font-semibold text-foreground">
              {new Date(asteroid.close_approach_date).toLocaleDateString(
                "en-US"
              )}
            </p>
          </div>
        </div>

        <div className="flex items-center justify-between pt-2">
          <Badge className={cn("font-medium", threatColors[threatLevel])}>
            <Rocket className="h-3 w-3 mr-1" />
            {threatLabels[threatLevel]}
          </Badge>
          <Button
            variant="outline"
            size="sm"
            onClick={() => onViewDetails(asteroid)}
            className="border-primary/50 hover:bg-primary/10 hover:text-primary hover:border-primary transition-all"
          >
            <Info className="h-4 w-4 mr-1" />
            View Details
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

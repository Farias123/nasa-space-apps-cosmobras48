import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { Filter } from "lucide-react";

interface FilterSidebarProps {
  maxDistance: number;
  onDistanceChange: (distance: number) => void;
}

export const FilterSidebar = ({
  maxDistance,
  onDistanceChange,
}: FilterSidebarProps) => {
  return (
    <Card className="glass-card sticky top-4">
      <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <Filter className="h-5 w-5 text-primary" />
              Filters
            </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <Label className="text-sm font-semibold">Maximum Distance</Label>
            <span className="text-xs text-muted-foreground">
              {maxDistance.toFixed(2)} AU
            </span>
          </div>
          <Slider
            value={[maxDistance]}
            onValueChange={([value]) => onDistanceChange(value)}
            min={0.01}
            max={15}
            step={0.01}
            className="cursor-pointer"
          />
            <div className="text-xs text-muted-foreground">
              Filter asteroids by maximum distance in Astronomical Units (AU)
            </div>
        </div>
      </CardContent>
    </Card>
  );
};

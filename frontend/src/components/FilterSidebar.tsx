import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { Badge } from '@/components/ui/badge';
import { ThreatLevel } from '@/types/asteroid';
import { Filter } from 'lucide-react';
import { cn } from '@/lib/utils';

interface FilterSidebarProps {
  selectedThreats: ThreatLevel[];
  onToggleThreat: (threat: ThreatLevel) => void;
  maxDistance: number;
  onDistanceChange: (distance: number) => void;
  minSize: number;
  onSizeChange: (size: number) => void;
}

const threatOptions: { value: ThreatLevel; label: string; color: string }[] = [
  { value: 'safe', label: 'Seguro', color: 'bg-success/20 text-success hover:bg-success/30' },
  { value: 'low', label: 'Baixo', color: 'bg-primary/20 text-primary hover:bg-primary/30' },
  { value: 'medium', label: 'Médio', color: 'bg-warning/20 text-warning hover:bg-warning/30' },
  { value: 'high', label: 'Alto', color: 'bg-destructive/20 text-destructive hover:bg-destructive/30' },
  { value: 'critical', label: 'Crítico', color: 'bg-destructive/30 text-destructive hover:bg-destructive/40' },
];

export const FilterSidebar = ({
  selectedThreats,
  onToggleThreat,
  maxDistance,
  onDistanceChange,
  minSize,
  onSizeChange,
}: FilterSidebarProps) => {
  return (
    <Card className="glass-card sticky top-4">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-lg">
          <Filter className="h-5 w-5 text-primary" />
          Filtros
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="space-y-3">
          <Label className="text-sm font-semibold">Nível de Ameaça</Label>
          <div className="flex flex-wrap gap-2">
            {threatOptions.map((threat) => (
              <Badge
                key={threat.value}
                className={cn(
                  "cursor-pointer transition-all",
                  threat.color,
                  selectedThreats.includes(threat.value)
                    ? "ring-2 ring-primary"
                    : "opacity-50"
                )}
                onClick={() => onToggleThreat(threat.value)}
              >
                {threat.label}
              </Badge>
            ))}
          </div>
        </div>

        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <Label className="text-sm font-semibold">Distância Máxima</Label>
            <span className="text-xs text-muted-foreground">{maxDistance.toFixed(1)}M km</span>
          </div>
          <Slider
            value={[maxDistance]}
            onValueChange={([value]) => onDistanceChange(value)}
            min={0.01}
            max={15}
            step={0.1}
            className="cursor-pointer"
          />
        </div>

        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <Label className="text-sm font-semibold">Tamanho Mínimo</Label>
            <span className="text-xs text-muted-foreground">{minSize}m</span>
          </div>
          <Slider
            value={[minSize]}
            onValueChange={([value]) => onSizeChange(value)}
            min={0}
            max={1500}
            step={10}
            className="cursor-pointer"
          />
        </div>
      </CardContent>
    </Card>
  );
};

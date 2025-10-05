import { Asteroid } from "@/types/asteroid";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Orbit, MapPin, Calendar, TrendingUp } from "lucide-react";
import React, { useMemo, useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { OrbitControls, Line } from "@react-three/drei";

interface TrajectoryViewProps {
  asteroid: Asteroid | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export const TrajectoryView = ({
  asteroid,
  open,
  onOpenChange,
}: TrajectoryViewProps) => {
  if (!asteroid) return null;

  // Dados simplificados de órbita
  const orbitData = {
    perihelion: (asteroid.distance * 0.7).toFixed(2),
    aphelion: (asteroid.distance * 1.3).toFixed(2),
    eccentricity: (Math.random() * 0.3 + 0.1).toFixed(3),
    inclination: (Math.random() * 15 + 5).toFixed(1),
    period: (asteroid.distance * 0.5).toFixed(1),
  };

  const a = Math.max(0.5, Math.min(asteroid.distance * 2, 4));
  const b = Math.max(0.4, Math.min(asteroid.distance * 1.6, 3.5));
  const asteroidRadius = Math.max(0.05, Math.min(asteroid.size / 1000, 0.6));

  const ellipsePoints = useMemo(() => {
    const points: [number, number, number][] = [];
    const segments = 128;
    for (let i = 0; i <= segments; i++) {
      const t = (i / segments) * Math.PI * 2;
      points.push([a * Math.cos(t), b * Math.sin(t), 0]);
    }
    return points;
  }, [a, b]);

  const AsteroidMesh = () => {
    const ref = useRef<any>(null);
    useFrame(({ clock }) => {
      const t = clock.getElapsedTime() * 0.3;
      if (ref.current) {
        ref.current.position.x = a * Math.cos(t);
        ref.current.position.y = b * Math.sin(t);
        ref.current.position.z = 0;
      }
    });
    return (
      <mesh ref={ref}>
        <sphereGeometry args={[asteroidRadius, 32, 32]} />
        <meshStandardMaterial color="#8B4513" />
      </mesh>
    );
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="glass-card border-primary/30 max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold gradient-text">
            Trajetória Orbital
          </DialogTitle>
          <DialogDescription>
            Visualização da órbita e trajetória do asteroide {asteroid.name}
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6 mt-6">
          <div className="relative rounded-lg border border-primary/20 min-h-[360px] h-[360px]">
            <Canvas camera={{ position: [5, 5, 5], fov: 50 }}>
              <ambientLight intensity={0.5} />
              <directionalLight position={[5, 5, 5]} intensity={0.8} />
              <OrbitControls enablePan enableZoom enableRotate />

              <gridHelper args={[10, 20]} />
              <axesHelper args={[2]} />

              <mesh position={[0, 0, 0]}>
                <sphereGeometry args={[1, 32, 32]} />
                <meshStandardMaterial color="#4A90E2" />
              </mesh>

              <Line points={ellipsePoints} color="#22c55e" lineWidth={2} />

              <AsteroidMesh />
            </Canvas>
          </div>

          <Separator className="bg-border/50" />

          {/* Parâmetros Orbitais */}
          <div className="space-y-4">
            <h4 className="font-semibold text-lg flex items-center gap-2">
              <Orbit className="h-5 w-5 text-primary" />
              Parâmetros Orbitais
            </h4>

            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              <div className="glass-card p-4 space-y-1">
                <div className="flex items-center gap-2 text-muted-foreground">
                  <MapPin className="h-4 w-4 text-primary" />
                  <span className="text-sm">Periélio</span>
                </div>
                <p className="text-xl font-bold">{orbitData.perihelion}M km</p>
              </div>

              <div className="glass-card p-4 space-y-1">
                <div className="flex items-center gap-2 text-muted-foreground">
                  <MapPin className="h-4 w-4 text-primary" />
                  <span className="text-sm">Afélio</span>
                </div>
                <p className="text-xl font-bold">{orbitData.aphelion}M km</p>
              </div>

              <div className="glass-card p-4 space-y-1">
                <div className="flex items-center gap-2 text-muted-foreground">
                  <TrendingUp className="h-4 w-4 text-primary" />
                  <span className="text-sm">Excentricidade</span>
                </div>
                <p className="text-xl font-bold">{orbitData.eccentricity}</p>
              </div>

              <div className="glass-card p-4 space-y-1">
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Orbit className="h-4 w-4 text-primary" />
                  <span className="text-sm">Inclinação</span>
                </div>
                <p className="text-xl font-bold">{orbitData.inclination}°</p>
              </div>

              <div className="glass-card p-4 space-y-1">
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Calendar className="h-4 w-4 text-primary" />
                  <span className="text-sm">Período Orbital</span>
                </div>
                <p className="text-xl font-bold">{orbitData.period} anos</p>
              </div>

              <div className="glass-card p-4 space-y-1">
                <div className="flex items-center gap-2 text-muted-foreground">
                  <MapPin className="h-4 w-4 text-primary" />
                  <span className="text-sm">Tipo de Órbita</span>
                </div>
                <Badge className="bg-accent/20 text-accent mt-1">
                  {asteroid.orbit}
                </Badge>
              </div>
            </div>
          </div>

          <Separator className="bg-border/50" />

          {/* Informações de Aproximação */}
          <div className="space-y-3">
            <h4 className="font-semibold flex items-center gap-2">
              <Calendar className="h-4 w-4 text-primary" />
              Próximas Aproximações
            </h4>
            <div className="bg-accent/10 border border-accent/30 rounded-lg p-4 space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">
                  Próxima Aproximação:
                </span>
                <span className="font-semibold text-warning">
                  {new Date(asteroid.nextApproach).toLocaleDateString("pt-BR")}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">
                  Distância Mínima:
                </span>
                <span className="font-semibold">{asteroid.distance}M km</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">
                  Velocidade Relativa:
                </span>
                <span className="font-semibold">{asteroid.velocity} km/s</span>
              </div>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};

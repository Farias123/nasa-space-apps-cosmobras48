import React, { useMemo } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, Line } from "@react-three/drei";
import { CelestialBodyCloseApproachData } from "@/types/asteroid";
import {
  ImpactSimulationState,
  AsteroidTrajectory,
} from "@/types/impactSimulation";

interface ImpactSceneProps {
  asteroid: CelestialBodyCloseApproachData;
  simulationState: ImpactSimulationState;
  trajectory: AsteroidTrajectory;
}

// Componente da Terra
const Earth = () => (
  <mesh position={[0, 0, 0]}>
    <sphereGeometry args={[1, 32, 32]} />
    <meshStandardMaterial color="#4A90E2" roughness={0.8} metalness={0.2} />
  </mesh>
);

// Componente do Asteroide
const Asteroid = ({
  position,
  size = 0.1,
}: {
  position: { x: number; y: number; z: number };
  size?: number;
}) => (
  <mesh position={[position.x, position.y, position.z]}>
    <sphereGeometry args={[size, 16, 16]} />
    <meshStandardMaterial color="#8B4513" roughness={0.9} metalness={0.1} />
  </mesh>
);

// Componente da trajetória
const TrajectoryLine = ({ trajectory }: { trajectory: AsteroidTrajectory }) => {
  const trajectoryPoints = useMemo(() => {
    const points: [number, number, number][] = [];
    const segments = 50;

    for (let i = 0; i <= segments; i++) {
      const t = i / segments;
      const oneMinusT = 1 - t;

      const x =
        oneMinusT * oneMinusT * trajectory.startPosition.x +
        2 * oneMinusT * t * trajectory.controlPoints[0].x +
        t * t * trajectory.endPosition.x;

      const y =
        oneMinusT * oneMinusT * trajectory.startPosition.y +
        2 * oneMinusT * t * trajectory.controlPoints[0].y +
        t * t * trajectory.endPosition.y;

      const z =
        oneMinusT * oneMinusT * trajectory.startPosition.z +
        2 * oneMinusT * t * trajectory.controlPoints[0].z +
        t * t * trajectory.endPosition.z;

      points.push([x, y, z]);
    }

    return points;
  }, [trajectory]);

  return (
    <Line
      points={trajectoryPoints}
      color="#ff6b35"
      lineWidth={3}
      transparent
      opacity={0.7}
    />
  );
};

// Componente principal da cena
const SceneContent = ({
  asteroid,
  simulationState,
  trajectory,
}: ImpactSceneProps) => {
  // Calcular tamanho do asteroide baseado na velocidade
  const asteroidSize = useMemo(() => {
    const velocity = parseFloat(asteroid.velocity_kms);
    return Math.max(0.05, Math.min(velocity / 100, 0.3));
  }, [asteroid.velocity_kms]);

  return (
    <>
      {/* Iluminação */}
      <ambientLight intensity={0.4} />
      <directionalLight position={[5, 5, 5]} intensity={0.8} />
      <pointLight position={[-5, -5, -5]} intensity={0.3} />

      {/* Controles de órbita */}
      <OrbitControls
        enablePan={true}
        enableZoom={true}
        enableRotate={true}
        minDistance={3}
        maxDistance={20}
      />

      {/* Grade e eixos */}
      <gridHelper args={[10, 20]} />
      <axesHelper args={[2]} />

      {/* Terra */}
      <Earth />

      {/* Trajetória */}
      <TrajectoryLine trajectory={trajectory} />

      {/* Asteroide */}
      <Asteroid
        position={simulationState.asteroidPosition}
        size={asteroidSize}
      />

      {/* Informações do asteroide */}
      <mesh
        position={[
          simulationState.asteroidPosition.x + 0.5,
          simulationState.asteroidPosition.y + 0.5,
          simulationState.asteroidPosition.z,
        ]}
      >
        <planeGeometry args={[2, 1]} />
        <meshBasicMaterial color="#000000" transparent opacity={0.7} />
      </mesh>
    </>
  );
};

export const ImpactScene = ({
  asteroid,
  simulationState,
  trajectory,
}: ImpactSceneProps) => {
  return (
    <div className="w-full h-96 bg-gradient-to-br from-slate-900 to-slate-800 rounded-lg overflow-hidden">
      <Canvas
        camera={{
          position: [8, 6, 8],
          fov: 50,
        }}
        style={{ width: "100%", height: "100%" }}
      >
        <SceneContent
          asteroid={asteroid}
          simulationState={simulationState}
          trajectory={trajectory}
        />
      </Canvas>
    </div>
  );
};

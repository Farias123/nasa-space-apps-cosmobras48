import { useState, useCallback, useRef } from 'react';
import { CelestialBodyCloseApproachData } from '@/types/asteroid';
import { ImpactSimulationState, AsteroidTrajectory } from '@/types/impactSimulation';

export const useImpactSimulation = (asteroid: CelestialBodyCloseApproachData) => {
  const [state, setState] = useState<ImpactSimulationState>({
    isAnimating: false,
    animationProgress: 0,
    impactPoint: { x: 0, y: 0, z: 0 },
    asteroidPosition: { x: 0, y: 0, z: 0 },
  });

  const animationRef = useRef<number>();
  const startTimeRef = useRef<number>();

  // Calcular trajetória baseada nos dados do asteroide
  const calculateTrajectory = useCallback((): AsteroidTrajectory => {
    const distanceAu = parseFloat(asteroid.distance_au);
    const velocity = parseFloat(asteroid.velocity_kms);
    
    // Posição inicial do asteroide (baseada na distância AU)
    const startDistance = Math.max(2, distanceAu * 2); // Escala para visualização
    const startPosition = {
      x: startDistance,
      y: startDistance * 0.3, // Altura da trajetória
      z: 0,
    };

    // Ponto de impacto na Terra (centro)
    const endPosition = { x: 0, y: 0, z: 0 };

    // Pontos de controle para curva Bézier
    const controlPoints = [
      {
        x: startDistance * 0.7,
        y: startDistance * 0.5,
        z: startDistance * 0.2,
      },
      {
        x: startDistance * 0.3,
        y: startDistance * 0.2,
        z: -startDistance * 0.1,
      },
    ];

    return {
      startPosition,
      endPosition,
      controlPoints,
    };
  }, [asteroid.distance_au, asteroid.velocity_kms]);

  // Calcular posição do asteroide na trajetória
  const calculateAsteroidPosition = useCallback((progress: number) => {
    const trajectory = calculateTrajectory();
    const { startPosition, endPosition, controlPoints } = trajectory;

    // Curva de Bézier quadrática
    const t = Math.min(1, Math.max(0, progress));
    const oneMinusT = 1 - t;

    const x = 
      oneMinusT * oneMinusT * startPosition.x +
      2 * oneMinusT * t * controlPoints[0].x +
      t * t * endPosition.x;

    const y = 
      oneMinusT * oneMinusT * startPosition.y +
      2 * oneMinusT * t * controlPoints[0].y +
      t * t * endPosition.y;

    const z = 
      oneMinusT * oneMinusT * startPosition.z +
      2 * oneMinusT * t * controlPoints[0].z +
      t * t * endPosition.z;

    return { x, y, z };
  }, [calculateTrajectory]);

  // Iniciar animação
  const startSimulation = useCallback(() => {
    if (state.isAnimating) return;

    setState(prev => ({ ...prev, isAnimating: true, animationProgress: 0 }));
    startTimeRef.current = Date.now();

    const animate = () => {
      const elapsed = Date.now() - (startTimeRef.current || 0);
      const duration = 5000; // 5 segundos
      const progress = elapsed / duration;

      if (progress >= 1) {
        setState(prev => ({
          ...prev,
          isAnimating: false,
          animationProgress: 1,
        }));
        return;
      }

      const position = calculateAsteroidPosition(progress);
      setState(prev => ({
        ...prev,
        animationProgress: progress,
        asteroidPosition: position,
      }));

      animationRef.current = requestAnimationFrame(animate);
    };

    animationRef.current = requestAnimationFrame(animate);
  }, [state.isAnimating, calculateAsteroidPosition]);

  // Reiniciar simulação
  const resetSimulation = useCallback(() => {
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
    }
    
    setState({
      isAnimating: false,
      animationProgress: 0,
      impactPoint: { x: 0, y: 0, z: 0 },
      asteroidPosition: calculateAsteroidPosition(0),
    });
  }, [calculateAsteroidPosition]);

  // Exportar dados da simulação
  const exportData = useCallback(() => {
    const trajectory = calculateTrajectory();
    const data = {
      asteroid: {
        designation: asteroid.designation,
        velocity_kms: asteroid.velocity_kms,
        distance_au: asteroid.distance_au,
        close_approach_date: asteroid.close_approach_date,
      },
      simulation: {
        trajectory,
        finalPosition: state.asteroidPosition,
        animationProgress: state.animationProgress,
        timestamp: new Date().toISOString(),
      },
    };

    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: 'application/json',
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `impact-simulation-${asteroid.designation}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }, [asteroid, state, calculateTrajectory]);

  // Exportar PNG (placeholder - será implementado com canvas)
  const exportPNG = useCallback(() => {
    // TODO: Implementar captura de canvas como PNG
    console.log('Export PNG functionality will be implemented');
  }, []);

  return {
    state,
    trajectory: calculateTrajectory(),
    startSimulation,
    resetSimulation,
    exportData,
    exportPNG,
  };
};

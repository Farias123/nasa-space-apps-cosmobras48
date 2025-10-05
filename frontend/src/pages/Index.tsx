import { useState } from 'react';
import { Asteroid, ThreatLevel } from '@/types/asteroid';
import { mockAsteroids } from '@/data/mockAsteroids';
import { AsteroidCard } from '@/components/AsteroidCard';
import { FilterSidebar } from '@/components/FilterSidebar';
import { AsteroidDetails } from '@/components/AsteroidDetails';
import { AsteroidForm } from '@/components/AsteroidForm';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Plus, Search, Satellite, Star } from 'lucide-react';
import { toast } from 'sonner';

const Index = () => {
  const [asteroids, setAsteroids] = useState<Asteroid[]>(mockAsteroids);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedThreats, setSelectedThreats] = useState<ThreatLevel[]>([
    'safe',
    'low',
    'medium',
    'high',
    'critical',
  ]);
  const [maxDistance, setMaxDistance] = useState(15);
  const [minSize, setMinSize] = useState(0);
  const [selectedAsteroid, setSelectedAsteroid] = useState<Asteroid | null>(null);
  const [detailsOpen, setDetailsOpen] = useState(false);
  const [formOpen, setFormOpen] = useState(false);
  const [showFavoritesOnly, setShowFavoritesOnly] = useState(false);

  const handleToggleFavorite = (id: string) => {
    setAsteroids((prev) =>
      prev.map((asteroid) =>
        asteroid.id === id
          ? { ...asteroid, isFavorite: !asteroid.isFavorite }
          : asteroid
      )
    );
    toast.success('Favorito atualizado!');
  };

  const handleViewDetails = (asteroid: Asteroid) => {
    setSelectedAsteroid(asteroid);
    setDetailsOpen(true);
  };

  const handleToggleThreat = (threat: ThreatLevel) => {
    setSelectedThreats((prev) =>
      prev.includes(threat)
        ? prev.filter((t) => t !== threat)
        : [...prev, threat]
    );
  };

  const handleAddAsteroid = (asteroid: Asteroid) => {
    setAsteroids((prev) => [asteroid, ...prev]);
  };

  const filteredAsteroids = asteroids.filter((asteroid) => {
    const matchesSearch =
      asteroid.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      asteroid.id.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesThreat = selectedThreats.includes(asteroid.threatLevel);
    const matchesDistance = asteroid.distance <= maxDistance;
    const matchesSize = asteroid.size >= minSize;
    const matchesFavorite = !showFavoritesOnly || asteroid.isFavorite;

    return matchesSearch && matchesThreat && matchesDistance && matchesSize && matchesFavorite;
  });

  const favoriteCount = asteroids.filter((a) => a.isFavorite).length;

  return (
    <div className="min-h-screen pb-12">
      {/* Header */}
      <header className="sticky top-0 z-50 backdrop-blur-md bg-background/80 border-b border-border/50">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-primary/20 p-3 rounded-lg glow-primary">
                <Satellite className="h-8 w-8 text-primary" />
              </div>
              <div>
                <h1 className="text-3xl font-bold gradient-text">AstroWatch</h1>
                <p className="text-sm text-muted-foreground">
                  Sistema de Monitoramento de Asteroides
                </p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <Button
                variant={showFavoritesOnly ? 'default' : 'outline'}
                onClick={() => setShowFavoritesOnly(!showFavoritesOnly)}
                className="border-primary/50 hover:bg-primary/10"
              >
                <Star className={showFavoritesOnly ? 'fill-current' : ''} />
                Favoritos ({favoriteCount})
              </Button>
              <Button
                onClick={() => setFormOpen(true)}
                className="bg-primary hover:bg-primary/90 text-primary-foreground glow-primary"
              >
                <Plus className="h-4 w-4 mr-2" />
                Novo Asteroide
              </Button>
            </div>
          </div>

          {/* Search Bar */}
          <div className="mt-6 relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
            <Input
              placeholder="Buscar por nome ou ID do asteroide..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-12 bg-card/50 border-border/50 focus:border-primary h-12 text-base"
            />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 mt-8">
        <div className="flex gap-6">
          {/* Sidebar */}
          <aside className="w-64 flex-shrink-0">
            <FilterSidebar
              selectedThreats={selectedThreats}
              onToggleThreat={handleToggleThreat}
              maxDistance={maxDistance}
              onDistanceChange={setMaxDistance}
              minSize={minSize}
              onSizeChange={setMinSize}
            />
          </aside>

          {/* Asteroid Grid */}
          <main className="flex-1">
            <div className="mb-6">
              <h2 className="text-2xl font-bold">
                {showFavoritesOnly ? 'Asteroides Favoritos' : 'Todos os Asteroides'}
              </h2>
              <p className="text-muted-foreground mt-1">
                {filteredAsteroids.length} asteroide(s) encontrado(s)
              </p>
            </div>

            {filteredAsteroids.length === 0 ? (
              <div className="text-center py-16">
                <Satellite className="h-16 w-16 text-muted-foreground mx-auto mb-4 opacity-50" />
                <h3 className="text-xl font-semibold mb-2">Nenhum asteroide encontrado</h3>
                <p className="text-muted-foreground">
                  Tente ajustar os filtros ou adicionar um novo asteroide
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
                {filteredAsteroids.map((asteroid) => (
                  <AsteroidCard
                    key={asteroid.id}
                    asteroid={asteroid}
                    onToggleFavorite={handleToggleFavorite}
                    onViewDetails={handleViewDetails}
                  />
                ))}
              </div>
            )}
          </main>
        </div>
      </div>

      {/* Modals */}
      <AsteroidDetails
        asteroid={selectedAsteroid}
        open={detailsOpen}
        onOpenChange={setDetailsOpen}
        onToggleFavorite={handleToggleFavorite}
      />

      <AsteroidForm
        open={formOpen}
        onOpenChange={setFormOpen}
        onSubmit={handleAddAsteroid}
      />
    </div>
  );
};

export default Index;
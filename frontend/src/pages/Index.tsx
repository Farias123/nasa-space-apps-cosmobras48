import { useState } from "react";
import { CelestialBodyCloseApproachData } from "@/types/asteroid";
import { mockAsteroids } from "@/data/mockAsteroids";
import { AsteroidCard } from "@/components/AsteroidCard";
import { FilterSidebar } from "@/components/FilterSidebar";
import { AsteroidDetails } from "@/components/AsteroidDetails";
import { AsteroidForm } from "@/components/AsteroidForm";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Plus, Search, Satellite, Star } from "lucide-react";
import { toast } from "sonner";

const Index = () => {
  const [asteroids, setAsteroids] =
    useState<CelestialBodyCloseApproachData[]>(mockAsteroids);
  const [searchQuery, setSearchQuery] = useState("");
  const [maxDistance, setMaxDistance] = useState(15);
  const [selectedAsteroid, setSelectedAsteroid] =
    useState<CelestialBodyCloseApproachData | null>(null);
  const [detailsOpen, setDetailsOpen] = useState(false);
  const [formOpen, setFormOpen] = useState(false);

  const handleToggleFavorite = (designation: string) => {
    // For now, just show toast - favorite functionality will be implemented later
    toast.success("Favorite updated!");
  };

  const handleViewDetails = (asteroid: CelestialBodyCloseApproachData) => {
    setSelectedAsteroid(asteroid);
    setDetailsOpen(true);
  };

  const handleAddAsteroid = (asteroid: CelestialBodyCloseApproachData) => {
    setAsteroids((prev) => [asteroid, ...prev]);
  };

  const filteredAsteroids = asteroids.filter((asteroid) => {
    const matchesSearch = asteroid.designation
      .toLowerCase()
      .includes(searchQuery.toLowerCase());
    const distance = parseFloat(asteroid.distance_au);
    const matchesDistance = distance <= maxDistance;

    return matchesSearch && matchesDistance;
  });

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
                      Asteroid Monitoring System
                    </p>
                  </div>
            </div>
            <div className="flex items-center gap-3">
              <Button
                onClick={() => setFormOpen(true)}
                className="bg-primary hover:bg-primary/90 text-primary-foreground glow-primary"
              >
                  <Plus className="h-4 w-4 mr-2" />
                  New Asteroid
              </Button>
            </div>
          </div>

          {/* Search Bar */}
          <div className="mt-6 relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                <Input
                  placeholder="Search by asteroid designation..."
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
              maxDistance={maxDistance}
              onDistanceChange={setMaxDistance}
            />
          </aside>

          {/* Asteroid Grid */}
          <main className="flex-1">
            <div className="mb-6">
              <h2 className="text-2xl font-bold">All Asteroids</h2>
              <p className="text-muted-foreground mt-1">
                {filteredAsteroids.length} asteroid(s) found
              </p>
            </div>

            {filteredAsteroids.length === 0 ? (
              <div className="text-center py-16">
                <Satellite className="h-16 w-16 text-muted-foreground mx-auto mb-4 opacity-50" />
                <h3 className="text-xl font-semibold mb-2">
                  No asteroids found
                </h3>
                <p className="text-muted-foreground">
                  Try adjusting the filters or adding a new asteroid
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
                {filteredAsteroids.map((asteroid) => (
                  <AsteroidCard
                    key={asteroid.designation}
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

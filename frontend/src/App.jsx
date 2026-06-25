import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import MapComponent from './maps/MapComponent';
import Controls from './components/Controls';
import AnalyticsDashboard from './charts/AnalyticsDashboard';
import RecommendationsPanel from './components/RecommendationsPanel';
import LandingPage from './components/LandingPage';
import { fetchGraph, fetchRoute, fetchComparison } from './utils/api';
import { Network } from 'lucide-react';

function App() {
  const [showLanding, setShowLanding] = useState(true);
  const [graphData, setGraphData] = useState({ nodes: [], edges: [] });
  const [currentPath, setCurrentPath] = useState(null);
  const [stats, setStats] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [currentAlgorithm, setCurrentAlgorithm] = useState('');
  
  // Comparison state
  const [comparisonData, setComparisonData] = useState(null);
  const [isLoadingComparison, setIsLoadingComparison] = useState(false);
  
  // To store current search request params for comparison
  const [lastSearchParams, setLastSearchParams] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const data = await fetchGraph();
        setGraphData(data);
      } catch (error) {
        console.error("Failed to fetch graph data:", error);
      }
    };
    loadData();
  }, []);

  const handleSearch = async ({ start, goal, algorithm, constraints, preferences }) => {
    setIsLoading(true);
    setStats(null);
    setCurrentPath(null);
    setComparisonData(null);
    setCurrentAlgorithm(algorithm);
    setLastSearchParams({ start, goal, constraints, preferences });
    
    try {
      const result = await fetchRoute(start, goal, algorithm, constraints, preferences);
      if (result.success) {
        setCurrentPath(result.path);
        setStats(result);
      } else {
        alert(result.message || "Failed to find path");
      }
    } catch (error) {
      console.error("Search failed:", error);
      alert("Error executing search");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCompare = async () => {
    if (!lastSearchParams) return;
    setIsLoadingComparison(true);
    try {
      const data = await fetchComparison(
        lastSearchParams.start, 
        lastSearchParams.goal, 
        lastSearchParams.constraints,
        lastSearchParams.preferences
      );
      setComparisonData(data);
    } catch (error) {
      console.error("Comparison failed:", error);
      alert("Error executing comparison");
    } finally {
      setIsLoadingComparison(false);
    }
  };

  const currentDestination = currentPath && currentPath.length > 0 ? currentPath[currentPath.length - 1] : null;

  return (
    <AnimatePresence>
      {showLanding ? (
        <motion.div 
          key="landing"
          initial={{ opacity: 1 }}
          exit={{ opacity: 0, scale: 1.1, filter: "blur(10px)" }}
          transition={{ duration: 1 }}
        >
          <LandingPage onEnter={() => setShowLanding(false)} />
        </motion.div>
      ) : (
        <motion.div 
          key="app"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 0.5 }}
          className="w-screen h-screen bg-dark-bg text-white overflow-hidden flex flex-col p-4 relative font-sans"
        >
          {/* Background */}
          <div className="absolute inset-0 pointer-events-none z-0 bg-[#0a0a0a]"></div>

          {/* Header */}
          <header className="z-10 flex items-center justify-between mb-4 px-4 py-2 border-b border-white/5 bg-white/5 rounded-2xl backdrop-blur-md">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-neon-blue/10 border border-neon-blue/20 flex items-center justify-center shadow-[0_0_10px_rgba(0,243,255,0.2)]">
                <Network className="text-neon-blue" size={20} />
              </div>
              <div>
                <h1 className="text-xl font-bold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-400">NeuroTrip</h1>
                <p className="text-xs text-neon-pink font-medium mt-0.5 tracking-wider uppercase">AI Route Planner</p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="px-3 py-1.5 flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/20 rounded-full">
                <div className="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.5)] animate-pulse"></div>
                <span className="text-xs font-medium text-emerald-400">System Online</span>
              </div>
            </div>
          </header>

          {/* Main Layout */}
          <div className="flex-1 flex gap-4 h-[calc(100vh-100px)] z-10">
            
            {/* Left Side: Controls */}
            <div className="w-80 h-full flex-shrink-0">
              <Controls 
                nodes={graphData.nodes} 
                onSearch={handleSearch} 
                isLoading={isLoading} 
              />
            </div>
            
            {/* Center: Map */}
            <div className="flex-1 h-full relative rounded-2xl overflow-hidden border border-white/10 shadow-[0_0_30px_rgba(0,0,0,0.5)]">
              {isLoading && (
                <div className="absolute inset-0 z-20 bg-[#0a0a0a]/80 backdrop-blur-md flex flex-col items-center justify-center">
                  <div className="w-12 h-12 border-4 border-neon-blue/30 border-t-neon-blue rounded-full animate-spin"></div>
                  <p className="mt-4 text-neon-blue font-bold tracking-widest animate-pulse">FINDING OPTIMAL ROUTE...</p>
                </div>
              )}
              <MapComponent 
                nodes={graphData.nodes} 
                edges={graphData.edges} 
                path={currentPath}
                algorithm={currentAlgorithm}
              />
            </div>
            
            {/* Right Side: Analytics & Recommendations */}
            <div className="w-96 h-full flex-shrink-0 flex flex-col gap-4">
              <div className="flex-1 min-h-0">
                <AnalyticsDashboard 
                  stats={stats} 
                  comparisonData={comparisonData}
                  isLoadingComparison={isLoadingComparison}
                  onCompare={handleCompare}
                />
              </div>
              
              {/* Recommendations only show when a path is found and we have a destination */}
              {currentDestination && !comparisonData && (
                <div className="shrink-0 max-h-[40%]">
                  <RecommendationsPanel destination={currentDestination} />
                </div>
              )}
            </div>
            
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export default App;

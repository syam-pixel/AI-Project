import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { fetchRecommendations } from '../utils/api';
import { Star, MapPin, Coffee, Utensils, Building } from 'lucide-react';

const RecommendationsPanel = ({ destination }) => {
  const [recommendations, setRecommendations] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (!destination) return;
    
    const getRecs = async () => {
      setIsLoading(true);
      try {
        const data = await fetchRecommendations(destination);
        setRecommendations(data.recommendations || []);
      } catch (error) {
        console.error("Failed to fetch recommendations", error);
      } finally {
        setIsLoading(false);
      }
    };
    
    getRecs();
  }, [destination]);

  if (!destination) return null;

  if (isLoading) {
    return (
      <div className="mt-4 p-4 glass-panel flex flex-col items-center justify-center">
        <div className="w-8 h-8 border-2 border-neon-pink/30 border-t-neon-pink rounded-full animate-spin mb-2"></div>
        <span className="text-xs text-gray-400">Finding local hotspots...</span>
      </div>
    );
  }

  const getIcon = (type) => {
    switch (type) {
      case 'Hotel': return <Building size={14} className="text-neon-blue" />;
      case 'Restaurant': return <Utensils size={14} className="text-neon-orange" />;
      case 'Attraction': return <MapPin size={14} className="text-neon-pink" />;
      default: return <Coffee size={14} className="text-white" />;
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="mt-4 flex flex-col gap-3"
    >
      <h3 className="text-sm font-bold text-white flex items-center gap-2">
        <Star className="text-neon-orange" size={16} />
        Top Picks in {destination}
      </h3>
      
      <div className="grid grid-cols-1 gap-2 max-h-48 overflow-y-auto custom-scrollbar pr-1">
        {recommendations.map((rec, idx) => (
          <motion.div 
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: idx * 0.05 }}
            key={idx} 
            className="p-3 bg-white/5 border border-white/10 rounded-lg hover:bg-white/10 transition-colors flex items-center justify-between"
          >
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-black/40 flex items-center justify-center border border-white/5">
                {getIcon(rec.type)}
              </div>
              <div>
                <div className="text-sm font-medium text-white">{rec.name}</div>
                <div className="text-[10px] text-gray-400 uppercase tracking-wider">{rec.type}</div>
              </div>
            </div>
            <div className="flex items-center gap-1 bg-black/40 px-2 py-1 rounded-md border border-white/5">
              <Star size={10} className="text-amber-400 fill-amber-400" />
              <span className="text-xs font-bold text-white">{rec.rating}</span>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
};

export default RecommendationsPanel;

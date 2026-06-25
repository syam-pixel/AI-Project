import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Play, Settings2, ShieldAlert, Cpu, Search, ChevronDown, Sparkles } from 'lucide-react';

const SearchableSelect = ({ label, value, onChange, options, colorClass, focusClass }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useState("");
  const wrapperRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(event) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const filteredOptions = options.filter(opt => opt.toLowerCase().includes(search.toLowerCase()));

  return (
    <div className="relative" ref={wrapperRef}>
      <label className={`text-xs ${colorClass} uppercase tracking-wider mb-1 block`}>{label}</label>
      <div 
        className={`w-full bg-black/50 border border-dark-border rounded-lg p-2.5 text-white cursor-pointer transition-colors flex justify-between items-center ${isOpen ? focusClass : ''}`}
        onClick={() => {
            setIsOpen(!isOpen);
            if (!isOpen) setSearch("");
        }}
      >
        <span className="truncate">{value || "Select city..."}</span>
        <ChevronDown size={16} className="text-gray-400 flex-shrink-0" />
      </div>
      
      <AnimatePresence>
        {isOpen && (
          <motion.div 
            initial={{ opacity: 0, y: -5 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -5 }}
            transition={{ duration: 0.15 }}
            className="absolute z-50 w-full mt-1 bg-[#12121a] border border-dark-border rounded-lg shadow-2xl max-h-60 flex flex-col overflow-hidden backdrop-blur-xl"
          >
            <div className="flex items-center gap-2 p-2 border-b border-dark-border bg-black/40">
              <Search size={14} className="text-gray-400 ml-1 flex-shrink-0" />
              <input 
                type="text" 
                className="w-full bg-transparent text-sm text-white outline-none placeholder-gray-500"
                placeholder="Search city..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                autoFocus
              />
            </div>
            <div className="overflow-y-auto custom-scrollbar">
              {filteredOptions.length > 0 ? filteredOptions.map(opt => (
                <div 
                  key={opt} 
                  className={`p-2.5 hover:bg-white/10 cursor-pointer text-sm transition-colors ${value === opt ? colorClass + ' bg-white/5 font-medium' : 'text-gray-300'}`}
                  onClick={() => {
                    onChange(opt);
                    setIsOpen(false);
                  }}
                >
                  {opt}
                </div>
              )) : (
                <div className="p-3 text-sm text-gray-500 text-center">No city found</div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

const Controls = ({ nodes, onSearch, isLoading }) => {
  const [start, setStart] = useState('');
  const [goal, setGoal] = useState('');
  const [algorithm, setAlgorithm] = useState('A*');
  
  // Update defaults when nodes load
  useEffect(() => {
    if (nodes && nodes.length > 0) {
      if (!start || !nodes.find(n => n.id === start)) {
        setStart(nodes[0].id);
      }
      if (!goal || !nodes.find(n => n.id === goal)) {
        setGoal(nodes[nodes.length - 1].id);
      }
    }
  }, [nodes]);

  // CSP Constraints
  const [maxBudget, setMaxBudget] = useState(1000);
  const [maxTime, setMaxTime] = useState(50);
  const [maxTraffic, setMaxTraffic] = useState(0.8);
  const [maxWeather, setMaxWeather] = useState(0.8);

  // Minimax Preferences
  const [scenicWeight, setScenicWeight] = useState(1.0);
  const [safetyWeight, setSafetyWeight] = useState(1.0);
  const [costWeight, setCostWeight] = useState(1.0);
  
  const handleSearch = () => {
    onSearch({
      start,
      goal,
      algorithm,
      constraints: algorithm === 'CSP' ? {
        max_budget: maxBudget,
        max_time: maxTime,
        max_traffic: maxTraffic,
        max_weather: maxWeather
      } : {},
      preferences: algorithm === 'Minimax' ? {
        scenic_weight: scenicWeight,
        safety_weight: safetyWeight,
        cost_weight: costWeight,
        traffic_weight: 1.0,
        weather_weight: 1.0,
        crowd_weight: 1.0
      } : {}
    });
  };
  
  const nodeOptions = nodes.map(n => n.id).sort();
  const ALL_ALGORITHMS = ['BFS', 'DFS', 'UCS', 'Dijkstra', 'GBFS', 'Bidirectional', 'A*', 'CSP', 'Minimax'];
  
  return (
    <motion.div 
      initial={{ x: -50, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      className="glass-panel p-6 flex flex-col gap-6 h-full overflow-y-auto custom-scrollbar"
    >
      <div className="flex items-center gap-3 border-b border-dark-border pb-4">
        <Cpu className="text-neon-cyan" size={24} />
        <h2 className="text-xl font-bold tracking-wider text-white neon-text-blue">MISSION CONTROL</h2>
      </div>
      
      {/* Route Selection */}
      <div className="flex flex-col gap-4">
        <SearchableSelect 
          label="Origin"
          value={start}
          onChange={setStart}
          options={nodeOptions}
          colorClass="text-neon-cyan"
          focusClass="border-neon-cyan shadow-[0_0_10px_rgba(0,243,255,0.2)]"
        />
        
        <SearchableSelect 
          label="Destination"
          value={goal}
          onChange={setGoal}
          options={nodeOptions}
          colorClass="text-neon-pink"
          focusClass="border-neon-pink shadow-[0_0_10px_rgba(255,0,127,0.2)]"
        />
      </div>
      
      {/* Algorithm Selection */}
      <div>
        <label className="text-xs text-gray-400 uppercase tracking-wider mb-2 flex items-center gap-2">
          <Settings2 size={14} /> AI Core Algorithm
        </label>
        <div className="grid grid-cols-2 gap-2">
          {ALL_ALGORITHMS.map(alg => (
            <button
              key={alg}
              onClick={() => setAlgorithm(alg)}
              className={`p-2 rounded border text-xs font-medium transition-all ${
                algorithm === alg 
                ? 'bg-neon-cyan/20 border-neon-cyan text-neon-cyan neon-border-blue' 
                : 'bg-black/30 border-dark-border text-gray-400 hover:border-gray-500'
              }`}
            >
              {alg}
            </button>
          ))}
        </div>
      </div>
      
      {/* CSP Constraints */}
      {algorithm === 'CSP' && (
        <motion.div 
          initial={{ height: 0, opacity: 0 }}
          animate={{ height: 'auto', opacity: 1 }}
          className="flex flex-col gap-4 bg-black/30 p-4 rounded-lg border border-neon-purple/50"
        >
          <label className="text-xs text-neon-purple uppercase tracking-wider flex items-center gap-2">
            <ShieldAlert size={14} /> Hard Constraints
          </label>
          
          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-gray-400">Max Budget</span>
              <span className="text-neon-purple">${maxBudget}</span>
            </div>
            <input 
              type="range" min="100" max="2000" step="50"
              value={maxBudget} onChange={(e) => setMaxBudget(Number(e.target.value))}
              className="w-full accent-neon-purple"
            />
          </div>
          
          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-gray-400">Max Time</span>
              <span className="text-neon-purple">{maxTime}h</span>
            </div>
            <input 
              type="range" min="10" max="100" step="5"
              value={maxTime} onChange={(e) => setMaxTime(Number(e.target.value))}
              className="w-full accent-neon-purple"
            />
          </div>
          
          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-gray-400">Weather Risk Tolerance</span>
              <span className="text-neon-purple">{Math.round(maxWeather * 100)}%</span>
            </div>
            <input 
              type="range" min="0" max="1" step="0.1"
              value={maxWeather} onChange={(e) => setMaxWeather(Number(e.target.value))}
              className="w-full accent-neon-purple"
            />
          </div>
        </motion.div>
      )}

      {/* Minimax Preferences */}
      {algorithm === 'Minimax' && (
        <motion.div 
          initial={{ height: 0, opacity: 0 }}
          animate={{ height: 'auto', opacity: 1 }}
          className="flex flex-col gap-4 bg-black/30 p-4 rounded-lg border border-neon-pink/50"
        >
          <label className="text-xs text-neon-pink uppercase tracking-wider flex items-center gap-2">
            <Sparkles size={14} /> Utility Preferences
          </label>
          
          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-gray-400">Scenic Priority</span>
              <span className="text-neon-pink">{scenicWeight.toFixed(1)}x</span>
            </div>
            <input 
              type="range" min="0" max="3" step="0.1"
              value={scenicWeight} onChange={(e) => setScenicWeight(Number(e.target.value))}
              className="w-full accent-neon-pink"
            />
          </div>
          
          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-gray-400">Safety Priority</span>
              <span className="text-neon-pink">{safetyWeight.toFixed(1)}x</span>
            </div>
            <input 
              type="range" min="0" max="3" step="0.1"
              value={safetyWeight} onChange={(e) => setSafetyWeight(Number(e.target.value))}
              className="w-full accent-neon-pink"
            />
          </div>
          
          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-gray-400">Cost Aversion</span>
              <span className="text-neon-pink">{costWeight.toFixed(1)}x</span>
            </div>
            <input 
              type="range" min="0.1" max="3" step="0.1"
              value={costWeight} onChange={(e) => setCostWeight(Number(e.target.value))}
              className="w-full accent-neon-pink"
            />
          </div>
        </motion.div>
      )}
      
      {/* Execute Button */}
      <div className="mt-auto pt-4">
        <button 
          onClick={handleSearch}
          disabled={isLoading}
          className="w-full relative group overflow-hidden rounded-lg p-[1px]"
        >
          <span className="absolute inset-0 bg-gradient-to-r from-neon-blue via-neon-purple to-neon-pink opacity-70 group-hover:opacity-100 transition-opacity"></span>
          <div className="relative bg-dark-bg py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-all group-hover:bg-opacity-0">
            {isLoading ? (
              <span className="text-white font-bold tracking-widest animate-pulse">COMPUTING...</span>
            ) : (
              <>
                <Play className="text-white group-hover:text-black transition-colors" size={18} />
                <span className="text-white font-bold tracking-widest group-hover:text-black transition-colors">INITIALIZE</span>
              </>
            )}
          </div>
        </button>
      </div>
      
    </motion.div>
  );
};

export default Controls;

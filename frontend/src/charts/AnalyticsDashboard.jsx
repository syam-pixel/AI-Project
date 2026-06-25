import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, CartesianGrid } from 'recharts';
import { Activity, Clock, Map as MapIcon, DollarSign, Award, CheckCircle } from 'lucide-react';
import { fetchComparison } from '../utils/api';

const AnalyticsDashboard = ({ stats, comparisonData, isLoadingComparison, onCompare }) => {
  if (!stats && !comparisonData && !isLoadingComparison) {
    return (
      <div className="h-full glass-panel flex flex-col items-center justify-center p-6 text-center">
        <Activity className="w-16 h-16 text-white/20 mb-4" />
        <h3 className="text-xl font-bold text-white mb-2">No Data Available</h3>
        <p className="text-sm text-gray-400">Run a search or comparison to see analytics.</p>
      </div>
    );
  }

  if (isLoadingComparison) {
    return (
      <div className="h-full glass-panel flex flex-col items-center justify-center p-6 text-center">
        <div className="w-12 h-12 border-4 border-neon-blue/30 border-t-neon-blue rounded-full animate-spin mb-4"></div>
        <p className="text-neon-blue font-medium animate-pulse">Running full algorithm comparison...</p>
      </div>
    );
  }

  // If we have comparison data, show it
  if (comparisonData && comparisonData.comparisons) {
    const validComps = comparisonData.comparisons.filter(c => !c.error);
    
    // Process for chart
    const chartData = validComps.map(c => ({
      name: c.algorithm,
      Time: c.execution_time_ms,
      Nodes: c.nodes_explored,
      Cost: c.cost
    }));

    return (
      <div className="h-full glass-panel flex flex-col overflow-y-auto custom-scrollbar p-4 relative">
        <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2 sticky top-0 bg-dark-panel z-10 py-2 border-b border-white/10">
          <Award className="text-neon-pink" size={20} />
          Algorithm Comparison
        </h2>

        {/* Charts */}
        <div className="space-y-6">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="p-3 bg-white/5 rounded-xl border border-white/5">
            <h3 className="text-xs font-semibold text-gray-400 mb-2">Execution Time (ms) - Lower is better</h3>
            <div className="h-40">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 10, left: 10, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" horizontal={false} />
                  <XAxis type="number" stroke="#666" fontSize={10} />
                  <YAxis dataKey="name" type="category" stroke="#999" fontSize={10} width={80} />
                  <Tooltip contentStyle={{ backgroundColor: '#111', borderColor: '#333', color: '#fff' }} />
                  <Bar dataKey="Time" fill="#00f3ff" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </motion.div>

          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="p-3 bg-white/5 rounded-xl border border-white/5">
            <h3 className="text-xs font-semibold text-gray-400 mb-2">Nodes Explored - Lower is better</h3>
            <div className="h-40">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 10, left: 10, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" horizontal={false} />
                  <XAxis type="number" stroke="#666" fontSize={10} />
                  <YAxis dataKey="name" type="category" stroke="#999" fontSize={10} width={80} />
                  <Tooltip contentStyle={{ backgroundColor: '#111', borderColor: '#333', color: '#fff' }} />
                  <Bar dataKey="Nodes" fill="#9d00ff" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </motion.div>
        </div>

        {/* Winner Badges */}
        <div className="mt-6 space-y-3 pb-6">
          <h3 className="text-sm font-semibold text-gray-300 border-b border-white/10 pb-2">Algorithm Winners</h3>
          {validComps.filter(c => c.is_fastest).map(c => (
            <div key={`fast-${c.algorithm}`} className="flex items-center justify-between p-2 rounded-lg bg-neon-blue/10 border border-neon-blue/20">
              <span className="text-xs text-gray-400">Fastest</span>
              <span className="text-sm font-bold text-neon-blue">{c.algorithm} ({c.execution_time_ms}ms)</span>
            </div>
          ))}
          {validComps.filter(c => c.is_least_nodes).map(c => (
            <div key={`nodes-${c.algorithm}`} className="flex items-center justify-between p-2 rounded-lg bg-neon-purple/10 border border-neon-purple/20">
              <span className="text-xs text-gray-400">Most Efficient</span>
              <span className="text-sm font-bold text-neon-purple">{c.algorithm} ({c.nodes_explored} nodes)</span>
            </div>
          ))}
          {validComps.filter(c => c.is_lowest_cost).map(c => (
            <div key={`cost-${c.algorithm}`} className="flex items-center justify-between p-2 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
              <span className="text-xs text-gray-400">Optimal (Cost)</span>
              <span className="text-sm font-bold text-emerald-400">{c.algorithm} ({c.cost} cost)</span>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // Regular single search stats
  return (
    <div className="h-full glass-panel flex flex-col overflow-y-auto custom-scrollbar p-4">
      <div className="flex items-center justify-between mb-6 sticky top-0 bg-dark-panel z-10 py-2 border-b border-white/10">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <Activity className="text-neon-pink" size={20} />
          Route Analytics
        </h2>
        {onCompare && (
          <button 
            onClick={onCompare}
            className="text-xs px-3 py-1.5 bg-white/10 hover:bg-white/20 rounded-full transition-colors border border-white/10 text-white font-medium"
          >
            Compare All
          </button>
        )}
      </div>

      <div className="space-y-4">
        {/* Core Metrics */}
        <div className="grid grid-cols-2 gap-3">
          <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="p-3 rounded-xl bg-white/5 border border-white/10 flex flex-col">
            <span className="text-xs text-gray-400 flex items-center gap-1"><Clock size={12} /> Exec Time</span>
            <span className="text-lg font-bold text-neon-blue mt-1">{stats.execution_time_ms} ms</span>
          </motion.div>
          <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.05 }} className="p-3 rounded-xl bg-white/5 border border-white/10 flex flex-col">
            <span className="text-xs text-gray-400 flex items-center gap-1"><Network size={12} /> Explored</span>
            <span className="text-lg font-bold text-neon-purple mt-1">{stats.explored_nodes} nodes</span>
          </motion.div>
          <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.1 }} className="p-3 rounded-xl bg-white/5 border border-white/10 flex flex-col">
            <span className="text-xs text-gray-400 flex items-center gap-1"><MapIcon size={12} /> Distance</span>
            <span className="text-lg font-bold text-emerald-400 mt-1">{Math.round(stats.distance || 0)} km</span>
          </motion.div>
          <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.15 }} className="p-3 rounded-xl bg-white/5 border border-white/10 flex flex-col">
            <span className="text-xs text-gray-400 flex items-center gap-1"><DollarSign size={12} /> Travel Cost</span>
            <span className="text-lg font-bold text-amber-400 mt-1">${stats.cost}</span>
          </motion.div>
        </div>

        {/* Algorithm Badge */}
        <div className="mt-4 p-3 rounded-xl bg-gradient-to-r from-neon-blue/10 to-transparent border-l-2 border-neon-blue flex items-center justify-between">
          <div>
            <span className="text-xs text-neon-blue font-medium uppercase tracking-wider">Algorithm Used</span>
            <div className="text-lg font-bold text-white">{stats.algorithm || 'Unknown'}</div>
          </div>
          <div className="w-10 h-10 rounded-full bg-neon-blue/20 flex items-center justify-center">
            <CheckCircle className="text-neon-blue" size={20} />
          </div>
        </div>
        
        {/* Advanced Stats (Minimax / Uncertainty) */}
        {stats.utility_score !== undefined && (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="mt-4 p-4 rounded-xl bg-white/5 border border-white/10">
            <h3 className="text-sm font-semibold text-white mb-3">AI Utility Assessment</h3>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs text-gray-400">Utility Score</span>
              <span className="text-sm font-bold text-neon-pink">{stats.utility_score}</span>
            </div>
            {stats.uncertainty && (
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-400">Success Probability</span>
                <span className="text-sm font-bold text-emerald-400">{(stats.uncertainty.success_probability * 100).toFixed(1)}%</span>
              </div>
            )}
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default AnalyticsDashboard;

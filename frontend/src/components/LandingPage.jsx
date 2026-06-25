import React from 'react';
import { motion } from 'framer-motion';
import { Map, ArrowRight } from 'lucide-react';

const LinkedinIcon = ({ size = 24, className = "" }) => (
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    width={size} 
    height={size} 
    viewBox="0 0 24 24" 
    fill="none" 
    stroke="currentColor" 
    strokeWidth="2" 
    strokeLinecap="round" 
    strokeLinejoin="round" 
    className={className}
  >
    <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z" />
    <rect width="4" height="12" x="2" y="9" />
    <circle cx="4" cy="4" r="2" />
  </svg>
);

const LandingPage = ({ onEnter }) => {
  return (
    <div className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-[#0a0a0a] text-white overflow-hidden font-sans">
      {/* Subtle background glow */}
      <div className="absolute inset-0 pointer-events-none z-0">
        <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-blue-500/10 rounded-full blur-[120px]"></div>
        <div className="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-emerald-500/10 rounded-full blur-[120px]"></div>
      </div>
      
      {/* Central Content */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="z-10 flex flex-col items-center max-w-2xl text-center px-6"
      >
        <div className="w-16 h-16 mb-8 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center shadow-lg backdrop-blur-md">
          <Map className="text-blue-400" size={32} />
        </div>
        
        <h1 className="text-5xl md:text-6xl font-bold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-400 mb-6">
          NeuroTrip
        </h1>
        <p className="text-lg md:text-xl text-gray-400 mb-12 font-light leading-relaxed">
          An intelligent route planner designed to help you explore India optimally. 
          Discover the best paths based on distance, travel time, and real-time conditions.
        </p>
        
        <button 
          onClick={onEnter}
          className="group relative px-8 py-3.5 bg-white text-black hover:bg-gray-100 font-medium rounded-full transition-all duration-300 flex items-center gap-2 shadow-[0_0_20px_rgba(255,255,255,0.1)] hover:shadow-[0_0_30px_rgba(255,255,255,0.2)]"
        >
          <span>Start Planning</span>
          <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
        </button>
      </motion.div>
      
      {/* Footer / Credits */}
      <div className="absolute bottom-8 z-10 flex flex-col items-center opacity-70 hover:opacity-100 transition-opacity">
        <p className="text-xs text-gray-500 mb-3 font-medium">Built by</p>
        <a 
          href="https://www.linkedin.com/in/punyamanthula-sasya-syamala-26870237b/" 
          target="_blank" 
          rel="noopener noreferrer"
          className="flex items-center gap-2 text-gray-300 hover:text-white transition-colors duration-300"
        >
          <LinkedinIcon size={20} className="text-[#0a66c2]" />
          <span className="font-medium text-sm">Sasya Syamala</span>
        </a>
      </div>
    </div>
  );
};

export default LandingPage;

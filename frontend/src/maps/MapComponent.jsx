import React, { useEffect, useRef, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default marker icon in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Default Icon (Off State)
const defaultIcon = L.divIcon({
  className: 'custom-icon-off',
  html: `<div style="
    background-color: rgba(0, 243, 255, 0.15); 
    width: 6px; 
    height: 6px; 
    border-radius: 50%; 
  "></div>`,
  iconSize: [6, 6],
  iconAnchor: [3, 3]
});

// Custom Node Icon (Neon/Blink)
const createNeonIcon = (color) => {
  return L.divIcon({
    className: 'custom-icon-on',
    html: `<div class="node-blink" style="
      background-color: ${color}; 
      width: 14px; 
      height: 14px; 
      border-radius: 50%; 
      box-shadow: 0 0 15px ${color}, 0 0 30px ${color};
      border: 2px solid white;
    "></div>`,
    iconSize: [14, 14],
    iconAnchor: [7, 7]
  });
};

// Vehicle Icon
const vehicleIcon = L.divIcon({
  className: 'vehicle-icon',
  html: `<div style="
    background-color: #ffffff; 
    width: 16px; 
    height: 16px; 
    border-radius: 50%; 
    box-shadow: 0 0 20px #ffffff;
    border: 3px solid #00f3ff;
  "></div>`,
  iconSize: [16, 16],
  iconAnchor: [8, 8]
});

// Component to handle dynamic map bounds and vehicle movement
function PathAnimator({ pathEdges, nodes, edges, pathColor }) {
  const map = useMap();
  const [vehiclePos, setVehiclePos] = useState(null);
  const animationRef = useRef(null);
  
  useEffect(() => {
    if (!pathEdges || pathEdges.length === 0) {
      setVehiclePos(null);
      if (animationRef.current) cancelAnimationFrame(animationRef.current);
      return;
    }

    // 1. Zoom to fit the entire path
    const bounds = L.latLngBounds();
    const allPositions = [];

    pathEdges.forEach(pathEdge => {
      const u = pathEdge[0];
      const v = pathEdge[1];
      const sourceNode = nodes.find(n => n.id === u);
      const targetNode = nodes.find(n => n.id === v);
      if (!sourceNode || !targetNode) return;

      const edgeData = edges.find(e => 
        (e.source === u && e.target === v) || 
        (e.source === v && e.target === u)
      );

      let positions;
      if (edgeData && edgeData.geometry) {
         positions = edgeData.geometry;
      } else {
         positions = [
            [sourceNode.lat, sourceNode.lng],
            [targetNode.lat, targetNode.lng]
         ];
      }
      
      positions.forEach(pos => {
        bounds.extend(pos);
        allPositions.push(pos);
      });
    });

    if (allPositions.length > 0) {
      map.flyToBounds(bounds, { padding: [50, 50], duration: 1.5 });
    }

    // 2. Animate Vehicle
    if (allPositions.length > 1) {
      let currentIndex = 0;
      let progress = 0;
      const speed = 0.05; // Adjust speed

      const animate = () => {
        if (currentIndex >= allPositions.length - 1) {
          // Finished
          setVehiclePos(allPositions[allPositions.length - 1]);
          return;
        }

        const p1 = allPositions[currentIndex];
        const p2 = allPositions[currentIndex + 1];

        // Interpolate
        const lat = p1[0] + (p2[0] - p1[0]) * progress;
        const lng = p1[1] + (p2[1] - p1[1]) * progress;
        setVehiclePos([lat, lng]);

        progress += speed;
        if (progress >= 1) {
          progress = 0;
          currentIndex++;
        }

        animationRef.current = requestAnimationFrame(animate);
      };

      // Start animation after camera fly ends
      setTimeout(() => {
        animationRef.current = requestAnimationFrame(animate);
      }, 1500);
    }

    return () => {
      if (animationRef.current) cancelAnimationFrame(animationRef.current);
    };
  }, [pathEdges, nodes, edges, map]);

  return vehiclePos ? <Marker position={vehiclePos} icon={vehicleIcon} zIndexOffset={1000} /> : null;
}


const MapComponent = ({ nodes, edges, path, algorithm }) => {
  // Determine path edges
  const pathEdges = [];
  if (path && path.length > 1) {
    for (let i = 0; i < path.length - 1; i++) {
      pathEdges.push([path[i], path[i+1]]);
    }
  }

  // Choose color based on algorithm
  const pathColor = 
    algorithm === 'BFS' ? '#00f3ff' : // Cyan
    algorithm === 'DFS' ? '#ffaa00' : // Orange
    algorithm === 'UCS' ? '#0f0' :    // Green
    algorithm === 'A*' ? '#9d00ff' :  // Purple
    algorithm === 'Dijkstra' ? '#ff007f' : // Pink
    algorithm === 'Minimax' ? '#ffffff' : // White
    '#00f3ff';

  return (
    <div className="w-full h-full rounded-xl overflow-hidden shadow-[0_0_20px_rgba(0,243,255,0.15)] relative">
      <MapContainer 
        center={[22.0, 79.0]} 
        zoom={5} 
        minZoom={4}
        style={{ height: '100%', width: '100%', background: '#050510' }}
        zoomControl={false}
      >
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://carto.com/">CARTO</a>'
        />

        {/* Render base edges */}
        {edges && edges.map((edge, idx) => {
          const sourceNode = nodes.find(n => n.id === edge.source);
          const targetNode = nodes.find(n => n.id === edge.target);
          if (!sourceNode || !targetNode) return null;
          
          const positions = edge.geometry ? edge.geometry : [
            [sourceNode.lat, sourceNode.lng],
            [targetNode.lat, targetNode.lng]
          ];
          
          return (
            <Polyline 
              key={`edge-${idx}`}
              positions={positions}
              color="rgba(0, 243, 255, 0.05)"
              weight={1}
            />
          );
        })}

        {/* Render highlighted path */}
        {pathEdges.length > 0 && pathEdges.map((pathEdge, idx) => {
          const u = pathEdge[0];
          const v = pathEdge[1];
          const sourceNode = nodes.find(n => n.id === u);
          const targetNode = nodes.find(n => n.id === v);
          if (!sourceNode || !targetNode) return null;

          const edgeData = edges.find(e => 
            (e.source === u && e.target === v) || 
            (e.source === v && e.target === u)
          );

          let positions;
          if (edgeData && edgeData.geometry) {
             positions = edgeData.geometry;
          } else {
             positions = [
                [sourceNode.lat, sourceNode.lng],
                [targetNode.lat, targetNode.lng]
             ];
          }

          return (
            <Polyline 
              key={`path-${idx}`}
              positions={positions}
              color={pathColor}
              weight={4}
              opacity={0.8}
              dashArray="10, 15"
              className="path-animation"
            />
          );
        })}

        {/* Render nodes */}
        {nodes && nodes.map((node, idx) => {
          const isPathNode = path && path.includes(node.id);
          const activeIcon = isPathNode ? createNeonIcon(pathColor) : defaultIcon;
          
          return (
            <Marker 
              key={`node-${idx}`} 
              position={[node.lat, node.lng]}
              icon={activeIcon}
              zIndexOffset={isPathNode ? 500 : 0}
            >
              <Popup className="glass-popup">
                <div className="text-dark-bg font-bold p-1">
                  {node.id}
                </div>
              </Popup>
            </Marker>
          );
        })}

        {/* Path Animator handles camera bounds and vehicle movement */}
        <PathAnimator pathEdges={pathEdges} nodes={nodes} edges={edges} pathColor={pathColor} />

      </MapContainer>
      
      {/* Add CSS for path animation */}
      <style dangerouslySetInnerHTML={{__html: `
        .node-blink {
          animation: nodePulse 1.5s infinite alternate;
        }
        @keyframes nodePulse {
          0% { transform: scale(0.85); opacity: 0.7; }
          100% { transform: scale(1.15); opacity: 1; filter: brightness(1.2); }
        }
        .path-animation {
          stroke-dasharray: 10;
          animation: dash 20s linear infinite;
        }
        @keyframes dash {
          to {
            stroke-dashoffset: -1000;
          }
        }
        .leaflet-popup-content-wrapper {
          background: rgba(10, 10, 20, 0.8) !important;
          border: 1px solid rgba(0, 243, 255, 0.3);
          color: white !important;
          backdrop-filter: blur(5px);
        }
        .leaflet-popup-tip {
          background: rgba(10, 10, 20, 0.8) !important;
        }
        .leaflet-popup-content .text-dark-bg {
          color: white;
        }
      `}} />
    </div>
  );
};

export default MapComponent;

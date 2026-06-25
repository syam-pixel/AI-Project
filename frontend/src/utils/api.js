const API_BASE_URL = 'http://localhost:8000/api';

export const fetchGraph = async () => {
  const response = await fetch(`${API_BASE_URL}/graph`);
  if (!response.ok) throw new Error('Network response was not ok');
  return await response.json();
};

export const fetchRoute = async (start, goal, algorithm, constraints = {}, preferences = {}) => {
  const response = await fetch(`${API_BASE_URL}/search`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      start,
      goal,
      algorithm,
      constraints,
      preferences
    }),
  });
  if (!response.ok) throw new Error('Network response was not ok');
  return await response.json();
};

export const fetchComparison = async (start, goal, constraints = {}, preferences = {}) => {
  const response = await fetch(`${API_BASE_URL}/compare`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      start,
      goal,
      constraints,
      preferences
    }),
  });
  if (!response.ok) throw new Error('Network response was not ok');
  return await response.json();
};

export const fetchRecommendations = async (destination) => {
  const response = await fetch(`${API_BASE_URL}/recommendations?destination=${encodeURIComponent(destination)}`);
  if (!response.ok) throw new Error('Network response was not ok');
  return await response.json();
};

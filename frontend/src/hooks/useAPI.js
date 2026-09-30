import { useState, useEffect, useCallback } from 'react';
import { api } from '../services/api';
import { mockData } from '../services/mockData';

/**
 * Custom hook for API calls with fallback to mock data.
 * Falls back gracefully when backend is not available.
 */
export function useAPI(apiCall, mockCall, deps = []) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isUsingMock, setIsUsingMock] = useState(false);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await apiCall();
      setData(result);
      setIsUsingMock(false);
    } catch (err) {
      // Fallback to mock data
      try {
        const mockResult = mockCall();
        setData(mockResult);
        setIsUsingMock(true);
      } catch (mockErr) {
        setError(mockErr.message);
      }
    } finally {
      setLoading(false);
    }
  }, deps);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, isUsingMock, refetch: fetchData };
}

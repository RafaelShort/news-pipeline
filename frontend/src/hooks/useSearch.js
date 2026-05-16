import { useState, useEffect, useCallback } from "react";
import { gqlRequest } from "../graphql/client";
import { SEARCH_ARTICLES } from "../graphql/queries";

export function useSearch() {
  const [filters, setFilters] = useState({
    query: "",
    topic: null,
    category: null,
    language: null,
    sourceName: null,
    fromDate: null,
    toDate: null,
    page: 1,
    pageSize: 10,
  });

  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await gqlRequest(SEARCH_ARTICLES, filters);
      setResults(data.search);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const updateFilter = useCallback((key, value) => {
    setFilters((prev) => ({
      ...prev,
      [key]: value || null,
      page: 1,
    }));
  }, []);

  const setPage = useCallback((page) => {
    setFilters((prev) => ({ ...prev, page }));
  }, []);

  const resetFilters = useCallback(() => {
    setFilters({
      query: "",
      topic: null,
      category: null,
      language: null,
      sourceName: null,
      fromDate: null,
      toDate: null,
      page: 1,
      pageSize: 10,
    });
  }, []);

  return {
    filters,
    updateFilter,
    setPage,
    resetFilters,
    results,
    loading,
    error,
    refetch: fetchData,
  };
}

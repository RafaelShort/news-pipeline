import { useState } from "react";
import { Newspaper, Loader2, AlertCircle } from "lucide-react";
import { SearchBar } from "../components/SearchBar";
import { FacetPanel } from "../components/FacetPanel";
import { ArticleCard } from "../components/ArticleCard";
import { ArticleModal } from "../components/ArticleModal";
import { useSearch } from "../hooks/useSearch";
import { useStats } from "../hooks/useStats";

export function Home() {
  const {
    filters,
    updateFilter,
    setPage,
    resetFilters,
    results,
    loading,
    error,
  } = useSearch();

  const [selectedId, setSelectedId] = useState(null);
  const stats = useStats();

  const totalPages = results
    ? Math.ceil(results.total / results.pageSize)
    : 0;

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Newspaper className="text-primary-600" size={24} />
            <h1 className="text-xl font-bold text-gray-900">News Pipeline</h1>
          </div>
          {stats && (
            <span className="text-sm text-gray-500">
              {stats.totalArticles.toLocaleString()} artigos indexados
            </span>
          )}
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-6">
        <div className="mb-6">
          <SearchBar
            value={filters.query}
            onChange={(v) => updateFilter("query", v)}
            onReset={resetFilters}
          />
        </div>

        <div className="flex gap-6 items-start">
          <div className="w-64 shrink-0">
            <FacetPanel
              facets={results?.facets}
              filters={filters}
              onFilter={updateFilter}
            />
          </div>

          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between mb-4">
              <p className="text-sm text-gray-500">
                {loading
                  ? "Buscando..."
                  : `${results?.total ?? 0} resultados`}
              </p>
            </div>

            {loading && (
              <div className="flex justify-center py-16">
                <Loader2 className="animate-spin text-primary-500" size={32} />
              </div>
            )}

            {error && (
              <div className="flex items-center gap-3 bg-red-50 text-red-700
                              border border-red-200 rounded-xl p-4">
                <AlertCircle size={18} />
                <p className="text-sm">Erro ao buscar artigos: {error.message}</p>
              </div>
            )}

            {!loading && results?.articles && (
              <div className="space-y-4">
                {results.articles.length === 0 ? (
                  <div className="text-center py-16 text-gray-400">
                    <Newspaper size={40} className="mx-auto mb-3 opacity-30" />
                    <p>Nenhum artigo encontrado</p>
                  </div>
                ) : (
                  results.articles.map((article) => (
                    <ArticleCard
                      key={article.id}
                      article={article}
                      onClick={(a) => setSelectedId(a.id)}
                    />
                  ))
                )}
              </div>
            )}

            {totalPages > 1 && (
              <div className="flex justify-center gap-2 mt-8">
                <button
                  disabled={filters.page === 1}
                  onClick={() => setPage(filters.page - 1)}
                  className="px-4 py-2 border border-gray-300 rounded-lg text-sm
                             disabled:opacity-40 hover:bg-gray-50 transition-colors"
                >
                  Anterior
                </button>
                <span className="px-4 py-2 text-sm text-gray-600">
                  {filters.page} / {totalPages}
                </span>
                <button
                  disabled={filters.page === totalPages}
                  onClick={() => setPage(filters.page + 1)}
                  className="px-4 py-2 border border-gray-300 rounded-lg text-sm
                             disabled:opacity-40 hover:bg-gray-50 transition-colors"
                >
                  Próximo
                </button>
              </div>
            )}
          </div>
        </div>
      </main>

      {selectedId && (
        <ArticleModal
          articleId={selectedId}
          onClose={() => setSelectedId(null)}
        />
      )}
    </div>
  );
}

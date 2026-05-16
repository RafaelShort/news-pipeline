export function FacetPanel({ facets, filters, onFilter }) {
  if (!facets) return null;

  const sections = [
    { label: "Tópico",    key: "topic",      buckets: facets.topics },
    { label: "Categoria", key: "category",   buckets: facets.categories },
    { label: "Fonte",     key: "sourceName", buckets: facets.sources },
    { label: "Idioma",    key: "language",   buckets: facets.languages },
  ];

  return (
    <aside className="w-64 shrink-0 space-y-6">
      {sections.map(({ label, key, buckets }) => (
        <div key={key}>
          <h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">
            {label}
          </h3>
          <ul className="space-y-1">
            {buckets.map((bucket) => (
              <li key={bucket.key}>
                <button
                  onClick={() =>
                    onFilter(key, filters[key] === bucket.key ? null : bucket.key)
                  }
                  className={`w-full text-left flex justify-between items-center
                              px-3 py-1.5 rounded-lg text-sm transition-colors
                              ${
                                filters[key] === bucket.key
                                  ? "bg-primary-100 text-primary-700 font-medium"
                                  : "hover:bg-gray-100 text-gray-700"
                              }`}
                >
                  <span className="truncate">{bucket.key}</span>
                  <span className="ml-2 text-xs text-gray-400 shrink-0">
                    {bucket.count}
                  </span>
                </button>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </aside>
  );
}

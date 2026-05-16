import { formatDistanceToNow } from "date-fns";
import { ptBR } from "date-fns/locale";
import { X, ExternalLink, Tag } from "lucide-react";
import { useArticle } from "../hooks/useArticle";
import { cleanSummary, isValidEntity } from "../utils/textUtils";

export function ArticleModal({ articleId, onClose }) {
  const { article, loading } = useArticle(articleId);

  const summary = cleanSummary(article?.summaryGenerated);

  return (
    <div
      className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <div
        className="bg-white rounded-2xl max-w-2xl w-full max-h-[85vh]
                   overflow-y-auto shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {loading && (
          <div className="p-8 text-center text-gray-500">Carregando...</div>
        )}

        {article && (
          <div className="p-6">
            <div className="flex justify-between items-start gap-4 mb-4">
              <h2 className="text-xl font-bold text-gray-900">{article.title}</h2>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600 shrink-0"
              >
                <X size={20} />
              </button>
            </div>

            <div className="flex flex-wrap gap-2 text-xs text-gray-500 mb-4">
              <span className="font-medium">{article.sourceName}</span>
              <span>·</span>
              <span>
                {formatDistanceToNow(new Date(article.publishedAt), {
                  addSuffix: true,
                  locale: ptBR,
                })}
              </span>
              <span>·</span>
              {article.topicMain && (
                <span className="px-2 py-0.5 bg-primary-50 text-primary-700 rounded-full">
                  {article.topicMain}
                </span>
              )}
              <span className="px-2 py-0.5 bg-gray-100 rounded-full">
                {article.language?.toUpperCase()}
              </span>
            </div>

            {summary ? (
              <div className="bg-blue-50 border border-blue-100 rounded-lg p-4 mb-4">
                <p className="text-xs font-semibold text-blue-600 mb-1">
                  📝 Resumo gerado por IA
                </p>
                <p className="text-sm text-gray-700">{summary}</p>
              </div>
            ) : (
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-4">
                <p className="text-xs text-gray-400 italic">
                  Resumo não disponível para este artigo
                </p>
              </div>
            )}

            {article.topics?.length > 0 && (
              <div className="mb-4">
                <p className="text-xs font-semibold text-gray-500 mb-2">
                  🔷 Tópicos detectados
                </p>
                <div className="flex flex-wrap gap-2">
                  {article.topics.map((t, i) => (
                    <span
                      key={i}
                      className="text-xs px-2 py-1 bg-gray-100 rounded-full"
                    >
                      {t.topic}
                      <span className="ml-1 text-gray-400">
                        {(t.score * 100).toFixed(0)}%
                      </span>
                    </span>
                  ))}
                </div>
              </div>
            )}

            {article.entities?.filter((e) => isValidEntity(e.text)).length > 0 && (
              <div className="mb-4">
                <p className="text-xs font-semibold text-gray-500 mb-2">
                  🔍 Entidades encontradas
                </p>
                <div className="flex flex-wrap gap-1">
                  {article.entities
                    .filter((e) => isValidEntity(e.text))
                    .map((e, i) => (
                      <span
                        key={i}
                        className="inline-flex items-center gap-1 text-xs px-2 py-1
                                   bg-blue-50 text-blue-700 rounded-full"
                      >
                        <Tag size={10} />
                        {e.text}
                        {e.labelPt && (
                          <span className="text-blue-400">({e.labelPt})</span>
                        )}
                      </span>
                    ))}
                </div>
              </div>
            )}

            <a
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-sm text-primary-600
                         hover:text-primary-800 font-medium mt-2"
            >
              <ExternalLink size={14} />
              Ver artigo original
            </a>
          </div>
        )}
      </div>
    </div>
  );
}

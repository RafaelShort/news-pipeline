import { formatDistanceToNow } from "date-fns";
import { ptBR } from "date-fns/locale";
import { ExternalLink, Tag, BookOpen } from "lucide-react";
import { cleanSummary, isValidEntity } from "../utils/textUtils";

export function ArticleCard({ article, onClick }) {
  const published = article.publishedAt
    ? formatDistanceToNow(new Date(article.publishedAt), {
        addSuffix: true,
        locale: ptBR,
      })
    : "—";

  const summary = cleanSummary(article.summaryGenerated);
  const topEntities =
    article.entities?.filter((e) => isValidEntity(e.text)).slice(0, 3) || [];

  return (
    <article
      onClick={() => onClick(article)}
      className="bg-white rounded-xl border border-gray-200 p-5 cursor-pointer
                 hover:shadow-md hover:border-primary-300 transition-all"
    >
      <div className="flex items-start justify-between gap-3 mb-2">
        <h2 className="text-base font-semibold text-gray-900 leading-snug">
          {article.title}
        </h2>
        <a
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          onClick={(e) => e.stopPropagation()}
          className="text-gray-400 hover:text-primary-600 shrink-0 mt-0.5"
        >
          <ExternalLink size={16} />
        </a>
      </div>

      {summary ? (
        <p className="text-sm text-gray-600 mb-3 line-clamp-2">{summary}</p>
      ) : (
        <p className="text-sm text-gray-400 italic mb-3">
          Resumo não disponível para este artigo
        </p>
      )}

      {topEntities.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-3">
          {topEntities.map((ent, i) => (
            <span
              key={i}
              className="inline-flex items-center gap-1 text-xs px-2 py-0.5
                         bg-blue-50 text-blue-700 rounded-full"
            >
              <Tag size={10} />
              {ent.text}
            </span>
          ))}
        </div>
      )}

      <div className="flex items-center justify-between text-xs text-gray-400 mt-2">
        <div className="flex items-center gap-3">
          <span className="font-medium text-gray-500">{article.sourceName}</span>
          <span>{published}</span>
        </div>
        <div className="flex items-center gap-2">
          {article.topicMain && (
            <span className="px-2 py-0.5 bg-primary-50 text-primary-700
                             rounded-full font-medium">
              {article.topicMain}
            </span>
          )}
          <span className="flex items-center gap-1">
            <BookOpen size={12} />
            {article.wordCount} palavras
          </span>
        </div>
      </div>
    </article>
  );
}

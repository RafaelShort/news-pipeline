/**
 * Remove todas as tags HTML de uma string
 */
export function stripHtml(html) {
  if (!html) return "";
  return html.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
}

/**
 * Retorna o resumo limpo ou null se não for útil
 */
export function cleanSummary(raw) {
  if (!raw) return null;
  const text = stripHtml(raw);

  const useless = ["comments", "leia mais", "read more", "saiba mais", "clique aqui"];
  if (text.length < 30) return null;
  if (useless.some((u) => text.toLowerCase().trim() === u)) return null;

  return text;
}

/**
 * Valida se uma entidade é exibível
 */
export function isValidEntity(text) {
  if (!text) return false;
  if (/<[^>]*>/.test(text)) return false;
  if (text.startsWith("http")) return false;
  if (text.startsWith("/")) return false;
  if (text.startsWith("+")) return false;
  if (text.includes(".com")) return false;
  if (text.includes(".org")) return false;
  if (text.includes("=")) return false;
  if (text.includes(">")) return false;
  if (/^[a-f0-9]{8,}$/i.test(text)) return false;
  if (text.length > 40) return false;
  if (text.length < 2) return false;
  return true;
}

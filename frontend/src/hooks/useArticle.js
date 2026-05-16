import { useState, useEffect } from "react";
import { gqlRequest } from "../graphql/client";
import { GET_ARTICLE } from "../graphql/queries";

export function useArticle(id) {
  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    gqlRequest(GET_ARTICLE, { id })
      .then((data) => setArticle(data.article))
      .catch(() => setArticle(null))
      .finally(() => setLoading(false));
  }, [id]);

  return { article, loading };
}

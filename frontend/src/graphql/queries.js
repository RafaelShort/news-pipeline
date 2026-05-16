export const SEARCH_ARTICLES = `
  query SearchArticles(
    $query: String
    $topic: String
    $category: String
    $language: String
    $sourceName: String
    $fromDate: String
    $toDate: String
    $page: Int
    $pageSize: Int
  ) {
    search(
      filters: {
        query: $query
        topic: $topic
        category: $category
        language: $language
        sourceName: $sourceName
        fromDate: $fromDate
        toDate: $toDate
        page: $page
        pageSize: $pageSize
      }
    ) {
      total
      page
      pageSize
      articles {
        id
        title
        url
        summaryGenerated
        publishedAt
        sourceName
        topicMain
        language
        wordCount
        entities { text labelPt }
        topics { topic score }
      }
      facets {
        topics    { key count }
        categories { key count }
        sources   { key count }
        languages { key count }
      }
    }
  }
`;

export const GET_ARTICLE = `
  query GetArticle($id: String!) {
    article(id: $id) {
      id
      title
      url
      content
      summary
      summaryGenerated
      publishedAt
      processedAt
      sourceName
      topicMain
      language
      category
      wordCount
      entities { text label labelPt }
      topics { topic score }
    }
  }
`;

export const GET_STATS = `
  query GetStats {
    stats {
      totalArticles
    }
  }
`;

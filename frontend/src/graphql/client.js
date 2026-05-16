const GRAPHQL_URI = '/graphql';

export async function gqlRequest(query, variables = {}) {
  const response = await fetch(GRAPHQL_URI, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, variables }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const { data, errors } = await response.json();
  if (errors) throw new Error(errors[0].message);
  return data;
}

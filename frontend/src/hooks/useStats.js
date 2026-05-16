import { useState, useEffect } from "react";
import { gqlRequest } from "../graphql/client";
import { GET_STATS } from "../graphql/queries";

export function useStats() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    gqlRequest(GET_STATS)
      .then((data) => setStats(data.stats))
      .catch(() => {});
  }, []);

  return stats;
}
